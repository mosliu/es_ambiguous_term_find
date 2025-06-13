# ES 歧义词查询服务

这是一个用于从 Elasticsearch 中查询特定词语并分析其上下文的服务。

## 功能特点

- 支持多字段搜索
- 支持时间范围过滤
- 自动提取关键词上下文
- 结果去重和统计
- 支持大量数据的分页查询
- 支持作者发文数量统计和可视化

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
    "end_time": "2024-01-02 00:00:00",
    "context_chars": 50,  // 可选参数，指定关键词前后提取的字符数
    "max_results": 10000  // 可选参数，指定最大返回结果数
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
        "max_results": 10000,  // ES返回的实际结果数
        "words": [             // 去重后的词条列表，按出现次数降序排序
            {
                "word": "匹配内容",
                "count": 出现次数
            }
        ]
    }
}
```

### 作者统计接口

```
POST /api/author-stats
```

请求参数：
```json
{
    "start_time": "2024-01-01 00:00:00",
    "end_time": "2024-01-02 00:00:00",
    "top_n": 10  // 可选参数，指定显示的作者数量，默认为10
}
```

响应格式：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total_authors": 100,  // 总作者数
        "time_range": {
            "start": "2024-01-01 00:00:00",
            "end": "2024-01-02 00:00:00"
        },
        "top_authors": [       // 发文数量最多的作者列表
            {
                "author": "作者名称",
                "count": 发文数量
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
MAX_RESULTS=10000        // 默认最大返回结果数
CONTEXT_CHARS=50        // 默认关键词前后提取的字符数
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

### 作者统计功能

1. 访问 http://localhost:8000/author_stats.html 打开作者统计界面
2. 选择时间范围
3. 设置要显示的作者数量（可选）
4. 点击查询按钮
5. 查看作者发文数量统计图表

## 注意事项

- 时间格式必须是 `YYYY-MM-DD HH:MM:SS`
- 最大返回结果数可以通过请求参数 `max_results` 自定义，默认使用 `MAX_RESULTS` 配置值
- 关键词上下文长度可以通过请求参数 `context_chars` 自定义，默认使用 `CONTEXT_CHARS` 配置值
- 上下文长度和最大结果数的最小值均为1
- 作者统计功能支持自定义显示数量，最小值为1