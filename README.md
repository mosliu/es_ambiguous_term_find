# ES 歧义词查询服务

这是一个用于从 Elasticsearch 中查询特定词语并分析其上下文的服务。

## 功能特点

- 支持多字段搜索
- 支持时间范围过滤
- 自动提取关键词上下文
- 结果去重和统计
- 支持大量数据的分页查询

## API 接口

### 搜索接口

```
POST /api/search
```

请求参数：
```json
{
    "keyword": "搜索关键词",
    "start_time": "2024-01-01 00:00:00",
    "end_time": "2024-01-02 00:00:00"
}
```

响应格式：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 13771,        // 总匹配数
        "parsed": 12756,       // 已解析数
        "max_results": 10000,  // 最大结果数
        "words": [             // 去重后的词条列表
            {
                "word": "匹配内容",
                "count": 出现次数
            }
        ]
    }
}
```

## 配置说明

在 `.env` 文件中配置以下参数：

```env
# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# Elasticsearch 配置
ES_HOST=localhost
ES_PORT=9200
ES_USERNAME=elastic
ES_PASSWORD=your_password

# 搜索配置
MAX_RESULTS=10000        // 最大返回结果数
CONTEXT_CHARS=50        // 关键词前后提取的字符数
```

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env_example .env
# 编辑 .env 文件，填入实际配置
```

3. 运行服务：
```bash
python main.py
```

## 使用说明

1. 访问 http://localhost:8000 打开查询界面
2. 输入搜索关键词
3. 选择时间范围
4. 点击搜索按钮
5. 查看结果统计和匹配内容

## 注意事项

- 时间格式必须是 `YYYY-MM-DD HH:MM:SS`
- 最大返回结果数受 `MAX_RESULTS` 配置限制
- 关键词上下文长度受 `CONTEXT_CHARS` 配置限制