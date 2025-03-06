from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.api import main_router as main_api
import uvicorn

app = FastAPI()


app.mount("/uploads" , StaticFiles(directory="uploads"), name="uploads")
app.include_router(main_api)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://new.nsumt.uz",
    ],  # Разрешаем доступ с вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)