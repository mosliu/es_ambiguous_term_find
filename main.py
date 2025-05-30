import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from config.settings import API_HOST, API_PORT
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="ES模糊词查询服务",
    description="用于从ES中查询特定词语并分析其上下文的服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """服务启动时的初始化操作"""
    logger.info("服务启动中...")

@app.on_event("shutdown")
async def shutdown_event():
    """服务关闭时的清理操作"""
    logger.info("服务关闭中...")

if __name__ == "__main__":
    logger.info(f"服务启动在 http://{API_HOST}:{API_PORT}")
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    ) 