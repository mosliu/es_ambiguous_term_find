# ES 模糊词查询服务

这是一个用于从 Elasticsearch 中查询特定词语并分析其上下文的服务。

## 功能特点

- 支持多字段查询（title, content, retweet_title, retweet_content等）
- 支持时间范围查询（精确到秒）
- 支持按月索引自动切换
- 支持上下文分析（前后4个字符）
- 支持多线程处理
- 完整的日志记录
- RESTful API接口
- 错误处理和异常恢复

## 环境要求

- Python 3.8+
- Elasticsearch 7.x+

## 安装

1. 克隆项目
```bash
git clone [项目地址]
cd es_ambiguous_term_find
```

2. 创建虚拟环境并安装依赖
```bash
uv venv
.venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

## 使用方法

1. 启动服务
```bash
python main.py
```

2. API 调用示例
```bash
curl -X POST http://localhost:8000/api/search \
-H "Content-Type: application/json" \
-d '{
    "keyword": "搜索词",
    "start_time": "2024-01-01 00:00:00",
    "end_time": "2024-03-01 23:59:59"
}'
```

## 项目结构

```