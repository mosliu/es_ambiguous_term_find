# ES 模糊词查询服务

这是一个基于 FastAPI 和 Elasticsearch 的模糊词查询服务，用于从 ES 中查询特定词语并分析其上下文。

## 功能特点

1. 关键词搜索
   - 支持模糊匹配
   - 支持时间范围筛选
   - 支持上下文长度设置
   - 支持最大结果数限制

2. 作者统计
   - 统计指定时间范围内的作者发文数量
   - 支持显示数量设置
   - 按发文数量降序排序

3. 媒体统计
   - 统计指定时间范围内的媒体发文数量
   - 支持显示数量设置
   - 按发文数量降序排序

## 技术栈

- FastAPI
- Elasticsearch
- Vue.js
- Bootstrap
- Flatpickr (日期时间选择器)

## 安装和配置

1. 克隆项目
```bash
git clone [项目地址]
cd es_ambiguous_term_find
```

2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env_example .env
# 编辑 .env 文件，设置必要的环境变量
```

## 运行服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动

## API 接口

### 1. 搜索接口
- 路径：`/api/search`
- 方法：POST
- 参数：
  - keyword: 搜索关键词
  - start_time: 开始时间
  - end_time: 结束时间
  - context_chars: 上下文长度（可选）
  - max_results: 最大结果数（可选）

### 2. 作者统计接口
- 路径：`/api/author-stats`
- 方法：POST
- 参数：
  - start_time: 开始时间
  - end_time: 结束时间
  - top_n: 显示数量（可选，默认100）

### 3. 媒体统计接口
- 路径：`/api/media-stats`
- 方法：POST
- 参数：
  - start_time: 开始时间
  - end_time: 结束时间
  - top_n: 显示数量（可选，默认100）

## 页面说明

1. 搜索页面 (`/`)
   - 关键词搜索
   - 时间范围选择
   - 上下文长度设置
   - 最大结果数设置

2. 作者统计页面 (`/author_stats.html`)
   - 时间范围选择
   - 显示数量设置
   - 作者排名列表

3. 媒体统计页面 (`/media_stats.html`)
   - 时间范围选择
   - 显示数量设置
   - 媒体排名列表

## 注意事项

1. 时间格式
   - 所有时间格式必须为：`YYYY-MM-DD HH:MM:SS`
   - 支持手动输入和日期选择器

2. 索引命名规则
   - 索引格式：`qbYYYYMM1`
   - 例如：`qb2024031` 表示 2024年3月 的索引

3. 查询限制
   - 默认最大结果数：10000
   - 默认显示数量：100
   - 支持自定义设置

## 开发说明

1. 目录结构
```
.
├── api/            # API 路由
├── core/           # 核心服务
├── config/         # 配置文件
├── static/         # 静态文件
├── utils/          # 工具函数
├── logs/           # 日志文件
├── main.py         # 主程序
└── requirements.txt # 依赖列表
```

2. 日志
- 日志文件位于 `logs` 目录
- 按日期和模块分类记录

3. 错误处理
- 统一的错误处理机制
- 详细的错误日志记录
- 友好的错误提示

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[许可证类型]