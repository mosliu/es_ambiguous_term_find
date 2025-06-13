from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor
from config.settings import MAX_WORKERS, SEARCH_FIELDS, CONTEXT_CHARS, MAX_RESULTS
from core.es_client import ESClient
from utils.logger import get_logger
import re

logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        self.es_client = ESClient()

    def _clean_text(self, text: str) -> str:
        """清理文本，移除无法编码的字符"""
        # 移除 emoji 和其他特殊字符
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        # 移除代理对字符
        text = re.sub(r'[\ud800-\udfff]', '', text)
        return text

    def _extract_context(self, text: str, keyword: str, context_chars: int = CONTEXT_CHARS) -> str:
        """提取关键词前后的指定字符数"""
        try:
            index = text.find(keyword)
            if index == -1:
                return ""
            
            start = max(0, index - context_chars)
            end = min(len(text), index + len(keyword) + context_chars)
            
            return text[start:end]
        except Exception as e:
            logger.error(f"提取上下文失败: {str(e)}")
            return ""

    def _process_document(self, doc: Dict[str, Any], keyword: str, context_chars: int = CONTEXT_CHARS) -> List[str]:
        """处理单个文档，返回所有匹配的内容列表"""
        try:
            source = doc.get("_source", {})
            matches = []

            # 处理所有可能的字段
            for field in SEARCH_FIELDS:
                if field in source:
                    text = source[field]
                    if isinstance(text, str) and keyword in text:
                        # 清理文本
                        cleaned_text = self._clean_text(text)
                        if cleaned_text:
                            # 提取上下文
                            context = self._extract_context(cleaned_text, keyword, context_chars)
                            if context:
                                matches.append(context)

            return matches
        except Exception as e:
            logger.error(f"处理文档失败: {str(e)}")
            return []

    def search(self, keyword: str, start_time: str, end_time: str, context_chars: int = CONTEXT_CHARS, max_results: int = MAX_RESULTS) -> Dict[str, Any]:
        """搜索并处理结果"""
        try:
            # 记录搜索参数
            logger.info(f"开始搜索 - 关键词: {keyword}, 时间范围: {start_time} 至 {end_time}, 上下文长度: {context_chars}, 最大结果数: {max_results}")
            
            # 获取原始搜索结果
            results = self.es_client.search(keyword, start_time, end_time, max_results)
            
            # 记录搜索结果数量
            logger.info(f"ES返回原始结果数量: {len(results)}")
            
            # 使用线程池处理结果
            all_matches = []
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [
                    executor.submit(self._process_document, doc, keyword, context_chars)
                    for doc in results
                ]
                for future in futures:
                    try:
                        matches = future.result()
                        all_matches.extend(matches)
                    except Exception as e:
                        logger.error(f"处理结果失败: {str(e)}")

            # 获取总数（从ES响应中获取）
            total_hits = 0
            if results and len(results) > 0:
                total_hits = results[0].get("_source", {}).get("total_hits", 0)

            # 构建返回结果
            return {
                "total": total_hits,
                "parsed": len(all_matches),
                "max_results": len(results),
                "words": sorted(
                    [{"word": word, "count": count} for word, count in 
                     {word: all_matches.count(word) for word in all_matches}.items()],
                    key=lambda x: x["count"],
                    reverse=True
                )
            }

        except Exception as e:
            logger.error(f"搜索服务失败: {str(e)}")
            raise 

    def get_author_stats(self, start_time: str, end_time: str, top_n: int = 10) -> Dict[str, Any]:
        """获取指定时间范围内的作者统计信息"""
        try:
            # 记录统计参数
            logger.info(f"开始统计作者 - 时间范围: {start_time} 至 {end_time}, 显示数量: {top_n}")
            
            # 获取作者聚合结果
            results = self.es_client.get_author_aggregation(start_time, end_time, top_n)
            
            # 构建返回结果
            return {
                "total_authors": results.get("total_authors", 0),
                "time_range": {
                    "start": start_time,
                    "end": end_time
                },
                "top_authors": results.get("top_authors", [])
            }

        except Exception as e:
            logger.error(f"作者统计服务失败: {str(e)}")
            raise 

    def get_media_stats(self, start_time: str, end_time: str, top_n: int) -> Dict[str, Any]:
        """获取媒体统计信息"""
        try:
            result = self.es_client.get_media_aggregation(
                start_time=start_time,
                end_time=end_time,
                top_n=top_n
            )
            return result
        except Exception as e:
            logger.error(f"媒体统计服务失败: {str(e)}")
            raise 