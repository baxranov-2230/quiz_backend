from fastapi import APIRouter, Depends
from .upload import router as upload
from .image_add import router as add_image
from .random_choose import router as random_choose
from .results import router as check_test
from .create import router as create
from .create_by_image import router as create_image
from .start import router as start
from .delete import router as delete
from src.auth.utils import check_user_role


question_router = APIRouter(
    prefix="/question",
    tags=["Question"]
)

question_router.include_router(upload , dependencies=[Depends(check_user_role(["admin", "teacher"]))])
question_router.include_router(add_image, dependencies=[Depends(check_user_role(["admin", "teacher"]))])
question_router.include_router(random_choose, dependencies=[Depends(check_user_role(["admin", "teacher"]))])
question_router.include_router(check_test , dependencies=[Depends(check_user_role(["admin", "teacher"]))])
question_router.include_router(create , dependencies=[Depends(check_user_role(["admin", "teacher"]))])
question_router.include_router(create_image)
question_router.include_router(start)
question_router.include_router(delete)