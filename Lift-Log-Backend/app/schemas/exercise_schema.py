from __future__ import annotations

from models.exercise_model import ExerciseModel
from pydantic import BaseModel, ConfigDict
from services.pagination_service import PaginatedData


class GetExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    exercise_name: str
    muscle_group: list[str]
    category: str
    is_custom: bool

    @classmethod
    def from_model(cls, exercise_model: ExerciseModel) -> GetExerciseResponse:
        return cls(
            id=str(exercise_model.id),
            exercise_name=exercise_model.exercise_name,
            muscle_group=exercise_model.muscle_group,
            category=exercise_model.category,
            is_custom=exercise_model.is_custom,
        )


class CreateExerciseRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exercise_name: str
    muscle_group: list[str]
    category: str
    is_custom: bool


class CreateExerciseResponse(BaseModel):
    id: str
    exercise_name: str
    muscle_group: list[str]
    category: str
    is_custom: bool

    @classmethod
    def from_model(cls, exercise_model: ExerciseModel) -> CreateExerciseResponse:
        return cls(
            id=str(exercise_model.id),
            exercise_name=exercise_model.exercise_name,
            muscle_group=exercise_model.muscle_group,
            category=exercise_model.category,
            is_custom=exercise_model.is_custom,
        )


class ListExerciseResponse(BaseModel):
    data: list[GetExerciseResponse]
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def from_model(cls, exercises: PaginatedData) -> ListExerciseResponse:
        return ListExerciseResponse(
            data=[GetExerciseResponse.from_model(item) for item in exercises.items],
            page=exercises.page,
            page_size=exercises.page_size,
            total_pages=exercises.total_pages,
        )
