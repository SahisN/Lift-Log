from db import inject_postgres_session
from exercise_repo import ExerciseRepo
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_exercise_repo(
    db: AsyncSession = Depends(inject_postgres_session),
) -> ExerciseRepo:
    return ExerciseRepo(db)
