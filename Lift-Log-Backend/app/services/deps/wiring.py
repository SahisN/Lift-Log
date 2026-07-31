from fastapi import Depends
from repo.deps.wiring import get_exercise_repo
from repo.exercise_repo import ExerciseRepo
from services.exercise_service import ExerciseService


def get_exercise_service(
    exercise_repo: ExerciseRepo = Depends(get_exercise_repo),
) -> ExerciseService:
    return ExerciseService(exercise_repo)
