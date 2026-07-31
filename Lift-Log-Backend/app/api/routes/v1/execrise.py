from fastapi import Depends
from models.ids import ExerciseId
from schemas.exercise_schema import (
    CreateExerciseRequest,
    CreateExerciseResponse,
    GetExerciseResponse,
)
from services.deps.wiring import get_exercise_service
from services.exercise_service import (
    ExerciseService,
)

from api.routes.routers import exercise_router


@exercise_router.get(
    "/{exercise_id}", status_code=200, response_model=GetExerciseResponse
)
async def get_exercise(
    exercise_id: str, service: ExerciseService = Depends(get_exercise_service)
) -> GetExerciseResponse:
    exercise = await service.get_execrise(execrise_id=ExerciseId(exercise_id))
    return GetExerciseResponse.from_model(exercise)


@exercise_router.post("/create", status_code=201, response_model=CreateExerciseResponse)
async def save_execrise(
    payload: CreateExerciseRequest,
    service: ExerciseService = Depends(get_exercise_service),
) -> CreateExerciseResponse:
    exercise = await service.create_execrise(payload=payload)
    return CreateExerciseResponse.from_model(exercise)
