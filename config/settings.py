import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# ES配置
ES_HOST = os.getenv('ES_HOST', 'localhost')
ES_PORT = int(os.getenv('ES_PORT', 9200))
ES_USERNAME = os.getenv('ES_USERNAME', 'elastic')
ES_PASSWORD = os.getenv('ES_PASSWORD', '')

# API配置
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR', 'logs')

# 查询配置
MAX_RESULTS = int(os.getenv('MAX_RESULTS', 10000))
CONTEXT_CHARS = int(os.getenv('CONTEXT_CHARS', 4))
SCROLL_TIMEOUT = os.getenv('SCROLL_TIMEOUT', '5m')
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 1000))

# 线程配置
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 4))

# 查询字段配置
SEARCH_FIELDS = [
    'title',
    'content',
    'retweet_title',
    'retweet_content'
]

# 索引前缀
INDEX_PREFIX = 'qb'

# 错误重试配置
MAX_RETRIES = 3
RETRY_DELAY = 1  # 秒 