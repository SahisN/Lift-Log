from __future__ import annotations

from models.exercise_profile_model import ExerciseProfileModel
from models.ids import ProfileId, UserId
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class ExerciseProfileRepo:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save(
        self, exercise_profile: ExerciseProfileModel
    ) -> ExerciseProfileModel:
        try:
            self._db.add(exercise_profile)
            await self._db.flush()
            await self._db.refresh(exercise_profile)
            return exercise_profile

        except SQLAlchemyError:
            await self._db.rollback()
            raise

    async def get(self, id: ProfileId) -> ExerciseProfileModel | None:
        return await self._db(ExerciseProfileModel, id.value)

    async def list(
        self, user_id: UserId, limit: int = 20, offset: int = 0
    ) -> list[ExerciseProfileModel]:
        profile_list = await self._db.execute(
            select(ExerciseProfileModel)
            .where(ExerciseProfileModel.user_id == user_id)
            .order_by(ExerciseProfileModel)
            .limit(limit)
            .offset(offset)
        )

        return list(profile_list.scalars().all())

    async def count(self, user_id: UserId) -> int:
        rows = (
            select(func.count())
            .select_from(ExerciseProfileModel)
            .where(ExerciseProfileModel.user_id == user_id)
        )
        db_rows = await self._db.execute(rows)

        return db_rows.scalar_one()
