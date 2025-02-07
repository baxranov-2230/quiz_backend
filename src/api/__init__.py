from .auths import auth_router as auth
from fastapi import APIRouter


main_router = APIRouter()

main_router.include_router(auth)