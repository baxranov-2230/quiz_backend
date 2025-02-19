from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import main_router as main_api
import uvicorn

app = FastAPI()


app.mount("/uploads" , StaticFiles(directory="uploads"), name="uploads")
app.include_router(main_api)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)