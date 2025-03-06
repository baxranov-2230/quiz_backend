from .auths import auth_router as auth
from .question_bank import question_router as question 
from .organizations import organization_router as orgnazition
from fastapi import APIRouter, Depends
from src.auth.utils import check_user_role


main_router = APIRouter()

main_router.include_router(auth)
main_router.include_router(question , dependencies=[Depends(check_user_role(["admin", "teacher"]))])
main_router.include_router(orgnazition, dependencies=[Depends(check_user_role(["admin"]))])