import uvicorn
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Redis Tutorial API is running!"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
