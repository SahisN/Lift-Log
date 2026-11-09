from db import inject_postgres_session
from fastapi import Depends
from repos.exercise_profile_repo import ExerciseProfileRepo
from repos.exercise_repo import ExerciseRepo
from sqlalchemy.ext.asyncio import AsyncSession


def get_exercise_repo(
    db: AsyncSession = Depends(inject_postgres_session),
) -> ExerciseRepo:
    return ExerciseRepo(db)


def get_exercise_profile_repo(
    db: AsyncSession = Depends(inject_postgres_session),
) -> ExerciseProfileRepo:
    return ExerciseProfileRepo(db)
