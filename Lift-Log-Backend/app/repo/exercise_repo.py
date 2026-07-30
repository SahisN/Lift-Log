from uuid import UUID

from models.exercise_model import ExerciseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class ExerciseRepo:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, execrise: ExerciseModel) -> ExerciseModel:
        try:
            self._db.add(execrise)
            await self._db.flush()
            await self._db.refresh(execrise)
            return execrise

        except SQLAlchemyError:
            await self._db.rollback()
            raise

    async def get(self, id: UUID) -> ExerciseModel | None:
        return await self._db.get(ExerciseModel, id)

    async def list(self, limit: int = 20, offset: int = 0) -> list[ExerciseModel]:
        result = await self._db.execute(
            select(ExerciseModel)
            .order_by(ExerciseModel.execrise_name)
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all())
