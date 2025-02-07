from .delete import router as delete
from .login import router as login
from .logout import router as logout
from .singup import router as signup
from .refresh import router as refresh
from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_router.include_router(delete)
auth_router.include_router(login)
auth_router.include_router(logout)
auth_router.include_router(signup)
auth_router.include_router(refresh)
