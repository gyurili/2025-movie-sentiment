import asyncio
from fastapi import FastAPI
from api import router as api_router
from model.database import engine
from model.models import Base


app = FastAPI()

app.include_router(api_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ DB 테이블 생성 완료")

@app.get("/", summary="기본으로 세팅된 API입니다.")
async def root():
    return {"message": "영화 리뷰 서비스"}