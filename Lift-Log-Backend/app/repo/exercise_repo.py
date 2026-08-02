from __future__ import annotations

from models.exercise_model import ExerciseModel
from models.ids import ExerciseId
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class ExerciseRepo:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, exercise: ExerciseModel) -> ExerciseModel:
        try:
            self._db.add(exercise)
            await self._db.flush()
            await self._db.refresh(exercise)
            return exercise

        except SQLAlchemyError:
            await self._db.rollback()
            raise

    async def get(self, id: ExerciseId) -> ExerciseModel | None:
        return await self._db.get(ExerciseModel, id.value)

    async def list(self, limit: int = 20, offset: int = 0) -> list[ExerciseModel]:
        result = await self._db.execute(
            select(ExerciseModel)
            .order_by(ExerciseModel.exercise_name)
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all())

    async def count(self) -> int:
        rows = select(func.count()).select_from(ExerciseModel)
        db_rows = await self._db.execute(rows)

        return db_rows.scalar_one()
