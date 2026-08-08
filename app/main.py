import uvicorn
from fastapi import FastAPI, status
import redis

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


if __name__ == "__main__":

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
