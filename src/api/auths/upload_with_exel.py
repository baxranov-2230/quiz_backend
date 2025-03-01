from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import pandas as pd
from src.model import Student, User, UserRole, Group, Teacher, Department
from src.settings.base import get_db
from src.auth.utils import generate_password

router = APIRouter()

@router.post("/upload_excel_student")
async def upload_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload an Excel file.")
    
    df = pd.read_excel(file.file)
    
    required_columns = {"first_name", "last_name", "patronymic", "jshir", "passport", "role"}
    if not required_columns.issubset(set(df.columns)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required columns in Excel file"
        )

    users = []
    students = []
    teachers = []
    
    for _, row in df.iterrows():
        # Check for duplicate JSHIR
        result = await db.execute(select(Student).where(Student.jshir == str(row["jshir"])))
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"JSHIR {row['jshir']} already exists"
            )

        # Check for duplicate passport
        existing_passport = await db.execute(select(User).where(User.username == row["passport"]))
        if existing_passport.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with passport {row['passport']} already exists"
            )

        # Validate role
        try:
            user_role = UserRole(row["role"])
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {row['role']}")

        # Create user
        user = User(
            username=row["passport"],
            hashed_password=await generate_password(),
            role=user_role,
            disabled=False
        )
        db.add(user)
        await db.flush()  # Ensure user.id is generated

        if user_role == UserRole.student:
            if "group" not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing 'group' column for students"
                )

            group_result = await db.execute(select(Group).where(Group.name == row["group"]))
            group = group_result.scalars().first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Group {row['group']} does not exist"
                )

            student = Student(
                first_name=row["first_name"],
                last_name=row["last_name"],
                patronymic=row["patronymic"],
                group_id=group.id,
                jshir=str(row["jshir"]),
                passport=row["passport"],
                user_id=user.id
            )
            students.append(student)

        elif user_role == UserRole.teacher:
            if "department" not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing 'department' column for teachers"
                )

            department_result = await db.execute(select(Department).where(Department.name == row["department"]))
            department = department_result.scalars().first()
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Department {row['department']} does not exist"
                )

            teacher = Teacher(
                first_name=row["first_name"],
                last_name=row["last_name"],
                patronymic=row["patronymic"],
                jshir=str(row["jshir"]),
                user_id=user.id,
                department_id=department.id,
                passport = row["passport"]
            )
            teachers.append(teacher)

        users.append(user)

    db.add_all(users + students + teachers)
    await db.commit()
    
    return {"message": "Data successfully uploaded"}
