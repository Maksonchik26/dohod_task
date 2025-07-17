import uvicorn
from fastapi import FastAPI

from app.routers.tasks import router as task_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
