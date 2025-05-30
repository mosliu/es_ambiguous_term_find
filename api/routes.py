from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from core.search_service import SearchService
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
search_service = SearchService()

class SearchRequest(BaseModel):
    keyword: str
    start_time: str
    end_time: str
    context_chars: Optional[int] = None

    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            return v
        except ValueError:
            raise ValueError("日期格式必须是 YYYY-MM-DD HH:MM:SS")

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v: str, info) -> str:
        if 'start_time' in info.data:
            start = datetime.strptime(info.data['start_time'], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            if end < start:
                raise ValueError("结束时间不能早于开始时间")
        return v

    @field_validator('context_chars')
    @classmethod
    def validate_context_chars(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError("上下文长度必须大于等于1")
        return v

@router.post("/search")
async def search(request: SearchRequest):
    """搜索接口"""
    try:
        # 执行搜索
        result = search_service.search(
            keyword=request.keyword,
            start_time=request.start_time,
            end_time=request.end_time,
            context_chars=request.context_chars
        )
        
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"搜索接口错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "code": 200,
        "message": "service is healthy",
        "timestamp": datetime.now().isoformat()
    } 