from fastapi import FastAPI
from src.api import main_router as main_api
import uvicorn

app = FastAPI()

app.include_router(main_api)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)