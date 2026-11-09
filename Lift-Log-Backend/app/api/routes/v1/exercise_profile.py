from fastapi import Depends, Query

from api.routes.routers import exercise_profile_router
from schemas.exercise_profile_schema import GetExerciseProfileResponse, CreateExerciseProfileResponse, \
    CreateExerciseProfileRequest
from services.exercise_profile_service import ExerciseProfileService
from services.deps.wiring import get_exercise_profile_service
from models.ids import ProfileId, UserId


@exercise_profile_router.get("/{exercise_id}", status_code=200, response_model=GetExerciseProfileResponse)
async def get_exercise_profile(
        profile_id: str,
        user_id: str,
        service: ExerciseProfileService = Depends(get_exercise_profile_service)
) -> GetExerciseProfileResponse:
    exercise_profile = await service.get_exercise_profile(ProfileId(profile_id), UserId(user_id))
    return GetExerciseProfileResponse.from_model(exercise_profile)

@exercise_profile_router.post("/create", status_code=201, response_model=GetExerciseProfileResponse)
async def save_exercise_profile(
        payload: CreateExerciseProfileRequest,
        service: ExerciseProfileService = Depends(get_exercise_profile_service)
) -> GetExerciseProfileResponse:
    exercise = await service.create_exercise_profile(payload=payload)
    return GetExerciseProfileResponse.from_model(exercise)