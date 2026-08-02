from fastapi import Depends, Query
from models.ids import ExerciseId
from schemas.exercise_schema import (
    CreateExerciseRequest,
    CreateExerciseResponse,
    GetExerciseResponse,
    ListExerciseResponse,
)
from services.deps.wiring import get_exercise_service
from services.exercise_service import (
    ExerciseService,
)

from api.routes.routers import exercise_router


@exercise_router.get("/exercises", status_code=200, response_model=ListExerciseResponse)
async def list_exercise(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=30),
    service: ExerciseService = Depends(get_exercise_service),
) -> ListExerciseResponse:
    exercises = await service.list_exercise(page=page, page_size=page_size)
    return ListExerciseResponse.from_model(exercises)


@exercise_router.get(
    "/{exercise_id}", status_code=200, response_model=GetExerciseResponse
)
async def get_exercise(
    exercise_id: str, service: ExerciseService = Depends(get_exercise_service)
) -> GetExerciseResponse:
    exercise = await service.get_exercise(execrise_id=ExerciseId(exercise_id))
    return GetExerciseResponse.from_model(exercise)


@exercise_router.post("/create", status_code=201, response_model=CreateExerciseResponse)
async def save_exercise(
    payload: CreateExerciseRequest,
    service: ExerciseService = Depends(get_exercise_service),
) -> CreateExerciseResponse:
    exercise = await service.create_exercise(payload=payload)
    return CreateExerciseResponse.from_model(exercise)
