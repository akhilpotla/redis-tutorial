import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import redis

from app.cache import get_cached_url, get_job_status
from app.models import Url
from app.queue import enqueue_url
from app.redis import r

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Redis Tutorial API is running!"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}


@app.get("/redis", status_code=status.HTTP_200_OK)
async def redis_check():
    try:
        r.ping()
        return {"status": "Redis is running!"}
    except redis.exceptions.ConnectionError as e:
        print("Error occurred while pinging Redis:", e)
        return {"status": "Redis is not running!"}


@app.post("/urls")
async def add_urls(url: Url):
    url_str = url.url
    value = await get_cached_url(url_str)
    if value:
        return value
    else:
        job_id = await enqueue_url(url_str)
        return job_id


@app.get("/job/{job_id}")
async def get_job(job_id: str):
    s = await get_job_status(job_id)
    if not s:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job ID not found"
        )
    return s


if __name__ == "__main__":

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
