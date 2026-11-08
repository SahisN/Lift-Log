from fastapi import Depends
from repos.deps.wiring import get_exercise_repo
from repos.exercise_repo import ExerciseRepo
from repos.exercise_profile_repo import ExerciseProfileRepo
from repos.deps.wiring import get_exercise_profile_repo

from services.exercise_profile_service import ExerciseProfileService
from services.exercise_service import ExerciseService
from services.pagination_service import PaginationService


def get_exercise_service(
    exercise_repo: ExerciseRepo = Depends(get_exercise_repo),
) -> ExerciseService:
    return ExerciseService(exercise_repo, PaginationService())

def get_exercise_profile_service(
        exercise_profile_repo: ExerciseProfileRepo = Depends(get_exercise_profile_repo)
) -> ExerciseProfileService:
    return ExerciseProfileService(exercise_profile_repo, PaginationService())