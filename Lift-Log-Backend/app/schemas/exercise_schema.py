from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class GetExerciseRequest(BaseModel):
    id: str


class GetExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    muscle_group: str
    category: str
    is_custom: bool


class CreateExerciseRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    muscle_group: str
    category: str
    is_custom: bool


class CreateExerciseResponse(BaseModel):
    id: str
    name: str
    muscle_group: str
    category: str
    is_custom: bool
