import asyncio
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.model import Question
from src.settings.base import get_db  

router = APIRouter()

@router.post("/upload")
async def upload_excel(file: UploadFile, db: AsyncSession = Depends(get_db)):
    try:
        
        loop = asyncio.get_running_loop()
        df = await loop.run_in_executor(None, pd.read_excel, file.file)
        df.columns = df.columns.str.strip()

        required_columns = {"Question", "A", "B", "C", "D"}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing_cols}"
            )

        uploaded_questions = []

        
        for _, row in df.iterrows():
            db_question = Question(
                text=row["Question"],
                A=row["A"],
                B=row["B"],
                C=row["C"],
                D=row["D"],
            )
            db.add(db_question)
            uploaded_questions.append({
                "question_text": row["Question"],
                "option_a": row["A"],
                "option_b": row["B"],
                "option_c": row["C"],
                "option_d": row["D"],
            })

        await db.commit()
        return uploaded_questions

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
