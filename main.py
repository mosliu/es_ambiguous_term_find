import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from config.settings import API_HOST, API_PORT
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="ES 模糊词查询服务",
    description="用于从 Elasticsearch 中查询特定词语并分析其上下文的服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """重定向到静态页面"""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

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