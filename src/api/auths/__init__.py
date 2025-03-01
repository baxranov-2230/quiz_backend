from .delete import router as delete
from .login import router as login
from .logout import router as logout
from .singup import router as signup
from .refresh import router as refresh
from .upload_with_exel import router as upload_with_exel
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
auth_router.include_router(upload_with_exel)
