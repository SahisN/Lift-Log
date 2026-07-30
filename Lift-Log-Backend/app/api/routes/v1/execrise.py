from fastapi import Depends
from models.ids import ExerciseId
from schemas.exercise_schema import GetExerciseResponse
from services.deps.wiring import get_exercise_service
from services.exercise_service import CreateExerciseRequest, ExerciseService

from api.routes.routers import exercise_router


@exercise_router.get("/exercise", status_code=200, response_model=GetExerciseResponse)
async def get_exercise(
    exercise_id: str, service: ExerciseService = Depends(get_exercise_service)
) -> GetExerciseResponse:
    exercise = await service.get_execrise(execrise_id=ExerciseId(exercise_id))
    return GetExerciseResponse.model_validate(exercise)


@exercise_router.post("/execrise", status_code=201, response_class=GetExerciseResponse)
async def save_execrise(
    payload: CreateExerciseRequest,
    service: ExerciseService = Depends(get_exercise_service),
) -> GetExerciseResponse:
    exercise = await service.create_execrise(payload=payload)
    return GetExerciseResponse.model_validate(exercise)
