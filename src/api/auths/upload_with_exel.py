from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.model import Student, User, UserRole, Group
from sqlalchemy.future import select
import pandas as pd
from src.settings.base import get_db
from src.auth.utils import generate_password

router = APIRouter()

@router.post("/upload_exel_student")
async def upload_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload an Excel file.")
    
    df = pd.read_excel(file.file)
    
    expected_columns = {"first_name", "last_name", "patronymic", "group", "jshir", "passport", "role"}
    if not expected_columns.issubset(set(df.columns)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid column names in Excel file"
        )    
    
    
    users = []
    students = []
    
    for _, row in df.iterrows():
        result = await db.execute(select(Student).where(Student.jshir == str(row["jshir"])))
        existing_student = result.scalars().first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"JSHIR {row['jshir']} already exists"
            )
        
        group_result = await db.execute(select(Group).where(Group.name == row["group"]))
        group = group_result.scalars().first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Group {row['group']} does not exist"
            )
        
        existing_passport = await db.execute(select(Student).where(Student.passport == row["passport"]))
        if existing_passport.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with passport {row['passport']} already exists"
            )
        try:
            user_role = UserRole(row["role"])
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {row['role']}")
        
        user = User(
            username=row["passport"],
            hashed_password=await generate_password(),
            role=user_role,
            disabled=False
        )
        db.add(user)
        await db.flush()  
        
        if user_role == UserRole.student:
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
    
    db.add_all(users + students)
    await db.commit()
    return {"message": "Data successfully uploaded"}
