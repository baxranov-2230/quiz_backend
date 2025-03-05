from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.settings.base import get_db
from src.model import UserTest, User, Teacher, Subject, Group
from src.auth.utils import get_current_user

router = APIRouter()

@router.post("/start")
async def start(
    group: str,
    subject: str,
    user_info: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user_info.role.value != "teacher" or user_info.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You not teacher"
        )

    results = await db.execute(
        select(Teacher, Subject, Group)
        .where(Teacher.user_id == user_info.id)
        .where(Subject.name == subject)
        .where(Group.name == group)
    )
    teacher, subject_obj, group_obj = results.first() or (None, None, None)


    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if not subject_obj:
        raise HTTPException(status_code=404, detail="Subject not found")
    if not group_obj:
        raise HTTPException(status_code=404, detail="Group not found")


    test_entry = UserTest(
        teacher_id=teacher.id,
        subject_id=subject_obj.id,
        group_id=group_obj.id,
    )

    db.add(test_entry)
    await db.commit()
    await db.refresh(test_entry)

    return test_entry
