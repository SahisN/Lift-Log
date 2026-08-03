from __future__ import annotations

import typing as t
from datetime import date

from models.exercise_profile_model import ExerciseProfileModel
from pydantic import BaseModel, ConfigDict
from services.pagination_service import PaginatedData

from schemas.exercise_schema import GetExerciseResponse


class CreateExerciseProfileRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: str
    exercise_id: str
    current_weight: float
    current_reps: int
    current_sets: int
    achieved_date: date


class CreateExerciseProfileResponse(BaseModel):
    pass


class GetExerciseProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    current_weight: int
    current_reps: int
    current_sets: int
    achieved_date: date
    exercise: GetExerciseResponse

    @classmethod
    def from_model(
        cls, exercise: GetExerciseResponse, exercise_profile: ExerciseProfileModel
    ) -> GetExerciseProfileResponse:
        return cls(
            id=str(exercise_profile.id),
            current_weight=exercise_profile.current_weight,
            current_reps=exercise_profile.current_reps,
            current_sets=exercise_profile.current_sets,
            achieved_date=exercise_profile.achieved_date,
            exercise=exercise,
        )


class ListExerciseProfileResponse(BaseModel):
    data: GetExerciseProfileResponse
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def from_model(
        cls, exercise_profiles: PaginatedData
    ) -> ListExerciseProfileResponse:
        return cls(
            data=[
                GetExerciseProfileResponse.from_model(item)
                for item in exercise_profiles.items
            ],
            page=exercise_profiles.page,
            page_size=exercise_profiles.page_size,
            total_pages=exercise_profiles.total_pages,
        )
