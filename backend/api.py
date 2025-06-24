from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.database import SessionLocal
from model.dto import MovieCreate, ReviewCreate, ReviewOut, SentimentRequest
from model.models import Movie, Review
from sentiment import analyze_sentiment


router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

# ---------------------------
# 영화 API
# ---------------------------

@router.get("/movies", summary="등록된 모든 영화의 목록을 반환합니다.")
async def get_movies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie))
    return result.scalars().all()

@router.post("/movies", summary="새로운 영화를 데이터베이스에 등록합니다.")
async def add_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    await db.commit()
    await db.refresh(new_movie)
    return new_movie

@router.get("/movies/{title}", summary="선택한 영화의 정보를 반환합니다.")
async def get_movie(title: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.title == title))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")
    return movie

@router.delete("/movies/{title}", summary="선택한 영화를 삭제합니다.")
async def delete_movie(title: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.title == title))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")
    await db.delete(movie)
    await db.commit()
    return {"message": "영화 삭제 완료"}

# ---------------------------
# 리뷰 및 감정 분석 API
# ---------------------------

@router.get("/movies/{title}/reviews", response_model=List[ReviewOut], summary="선택한 영화의 최근 리뷰 목록을 반환합니다.")
async def get_reviews(title: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.title == title))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="해당 영화 없음")

    result = await db.execute(
        select(Review).where(Review.movie_id == movie.id).order_by(Review.id.desc())
    )
    return result.scalars().all()[:10]

@router.post("/movies/{title}/reviews", summary="선택한 영화에 리뷰를 등록하고 감성 분석을 수행합니다.")
async def add_review(title: str, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.title == title))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="해당 영화 없음")

    sentiment = analyze_sentiment(review.content)
    new_review = Review(
        movie_id=movie.id,
        author=review.author,
        content=review.content,
        sentiment=sentiment["sentiment"],
        score=sentiment["score"]
    )
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

@router.delete("/movies/{title}/reviews/{review_id}", summary="선택한 영화의 특정 리뷰를 삭제합니다.")
async def delete_review(title: str, review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.title == title))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="해당 영화 없음")

    result = await db.execute(select(Review).where(Review.movie_id == movie.id, Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰 없음")

    await db.delete(review)
    await db.commit()
    return {"message": "리뷰 삭제 완료"}

@router.get("/movies/{title}/rating", summary="선택한 영화의 리뷰 평균 감성 점수를 계산하여 반환합니다.")
async def get_average_score(title: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.title == title))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="해당 영화 없음")

    result = await db.execute(select(Review).where(Review.movie_id == movie.id))
    reviews = result.scalars().all()
    if not reviews:
        return {"average_score": None, "message": "리뷰 없음"}
    
    avg = sum(r.score for r in reviews) / len(reviews)
    return {"average_score": round(avg, 2)}

@router.post("/predict", summary="리뷰의 감정을 분석하고 점수를 반환합니다.")
async def predict_sentiment(req: SentimentRequest):
    return analyze_sentiment(req.text, req.model_name or None)
