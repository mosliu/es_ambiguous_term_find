import json
from typing import Dict, List, Optional, Any
import requests
from requests.auth import HTTPBasicAuth
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime
from config.settings import (
    ES_HOST, ES_PORT, ES_USERNAME, ES_PASSWORD,
    SCROLL_TIMEOUT, MAX_RETRIES, RETRY_DELAY
)
from utils.logger import get_logger

logger = get_logger(__name__)

class ESClient:
    def __init__(self):
        self.base_url = f"http://{ES_HOST}:{ES_PORT}"
        self.auth = HTTPBasicAuth(ES_USERNAME, ES_PASSWORD) if ES_USERNAME and ES_PASSWORD else None
        self.headers = {"Content-Type": "application/json"}

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """发送请求到ES"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"ES请求失败: {str(e)}")
            raise

    def _validate_time_format(self, time_str: str) -> str:
        """验证并格式化时间字符串"""
        try:
            # 尝试解析时间字符串
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            # 返回格式化的时间字符串
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            logger.error(f"时间格式错误: {time_str}, 错误信息: {str(e)}")
            raise ValueError(f"时间格式必须为 'YYYY-MM-DD HH:MM:SS', 当前格式: {time_str}")

    def search_with_scroll(self, index: str, query: Dict, size: int = 1000) -> List[Dict]:
        """使用scroll API进行分页查询"""
        try:
            # 初始化scroll
            search_data = {
                "query": query,
                "size": size,
                "sort": ["_doc"],
                "track_total_hits": True
            }
            
            response = self._make_request("POST", f"{index}/_search?scroll={SCROLL_TIMEOUT}", search_data)
            scroll_id = response["_scroll_id"]
            hits = response["hits"]["hits"]
            total_hits = response["hits"]["total"]["value"]
            results = hits

            # 继续获取数据直到没有更多结果
            while hits and len(results) < 10000:  # 限制最大结果数
                scroll_data = {
                    "scroll": SCROLL_TIMEOUT,
                    "scroll_id": scroll_id
                }
                response = self._make_request("POST", "_search/scroll", scroll_data)
                hits = response["hits"]["hits"]
                results.extend(hits)

            # 清理scroll
            self._make_request("DELETE", "_search/scroll", {"scroll_id": scroll_id})
            
            # 添加总数信息到每个结果中
            for result in results:
                result["_source"] = result.get("_source", {})
                result["_source"]["total_hits"] = total_hits
            
            return results[:10000]  # 确保不超过最大限制

        except Exception as e:
            logger.error(f"Scroll查询失败: {str(e)}")
            raise

    def get_index_for_date(self, date_str: str) -> str:
        """根据日期获取对应的索引名"""
        # 假设date_str格式为 "YYYY-MM-DD"
        year = date_str[:4]
        month = date_str[5:7]
        return f"qb{year}{month}1"

    def search(self, keyword: str, start_time: str, end_time: str) -> List[Dict]:
        """搜索关键词"""
        try:
            # 验证并格式化时间
            start_time = self._validate_time_format(start_time)
            end_time = self._validate_time_format(end_time)
            
            # 构建查询
            query = {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase_prefix": {
                                            "title": {
                                                "query": keyword,
                                                "boost": 2
                                            }
                                        }
                                    },
                                    {
                                        "match_phrase_prefix": {
                                            "content": {
                                                "query": keyword
                                            }
                                        }
                                    },
                                    {
                                        "match_phrase_prefix": {
                                            "retweet_title": {
                                                "query": keyword,
                                                "boost": 2
                                            }
                                        }
                                    },
                                    {
                                        "match_phrase_prefix": {
                                            "retweet_content": {
                                                "query": keyword
                                            }
                                        }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        },
                        {
                            "range": {
                                "add_time": {
                                    "gte": start_time,
                                    "lte": end_time
                                }
                            }
                        }
                    ]
                }
            }

            # 获取时间范围内的所有索引
            start_index = self.get_index_for_date(start_time)
            end_index = self.get_index_for_date(end_time)
            
            logger.info(f"ES查询信息 - 查询语句: {json.dumps(query, ensure_ascii=False)}, "
                       f"开始索引: {start_index}, 结束索引: {end_index}")
            
            # 如果开始和结束索引相同，直接查询
            if start_index == end_index:
                results = self.search_with_scroll(start_index, query)
                logger.info(f"单索引查询完成 - 索引: {start_index}, 结果数量: {len(results)}")
                return results
            
            # 否则需要查询多个索引
            all_results = []
            current_index = start_index
            while current_index <= end_index:
                try:
                    results = self.search_with_scroll(current_index, query)
                    logger.info(f"多索引查询 - 当前索引: {current_index}, 结果数量: {len(results)}")
                    logger.info(f"返回的result为：{results}")
                    all_results.extend(results)
                except Exception as e:
                    logger.warning(f"查询索引 {current_index} 失败: {str(e)}")
                # 更新索引（这里需要根据实际的索引命名规则调整）
                current_index = self._get_next_index(current_index)
            
            logger.info(f"多索引查询完成 - 总结果数量: {len(all_results)}")
            return all_results[:10000]  # 确保不超过最大限制

        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            raise

    def _get_next_index(self, current_index: str) -> str:
        """获取下一个索引名"""
        # 这里需要根据实际的索引命名规则实现
        # 示例实现，实际应该根据月份递增
        year = current_index[2:6]
        month = int(current_index[6:8])
        if month == 12:
            year = str(int(year) + 1)
            month = 1
        else:
            month += 1
        return f"qb{year}{month:02d}1" 