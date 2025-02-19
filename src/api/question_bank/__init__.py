from fastapi import APIRouter
from .upload import router as upload
from .image_add import router as add_image
from .random_choose import router as random_choose
from .results import router as check_test
from .create import router as create
from .start import router as start
from .delete import router as delete

question_router = APIRouter(
    prefix="/question",
    tags=["Question"]
)

question_router.include_router(upload)
question_router.include_router(add_image)
question_router.include_router(random_choose)
question_router.include_router(check_test)
question_router.include_router(create)
question_router.include_router(start)
question_router.include_router(delete)