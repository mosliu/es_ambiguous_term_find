import sys
from pathlib import Path
from loguru import logger
from config.settings import LOG_LEVEL, LOG_DIR

# 创建日志目录
log_path = Path(LOG_DIR)
log_path.mkdir(exist_ok=True)

# 配置日志
logger.remove()  # 移除默认的处理器

# 添加控制台输出
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL,
    colorize=True
)

# 添加文件输出
logger.add(
    log_path / "app_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # 每天午夜创建新文件
    retention="30 days",  # 保留30天的日志
    compression="zip",  # 压缩旧日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=LOG_LEVEL,
    encoding="utf-8"
)

def get_logger(name: str):
    """获取指定名称的logger实例"""
    return logger.bind(name=name) 