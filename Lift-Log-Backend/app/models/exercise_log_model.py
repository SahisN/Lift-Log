from datetime import date
from uuid import UUID

from sqlalchemy import Date, Float, ForeignKey, Integer, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExerciseLogModel(Base):
    __tablename__ = "exercise_logs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    exercise_profile_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exercise_profiles.id"),
        nullable=False,
        index=True,
    )

    weight: Mapped[float] = mapped_column(Float, nullable=False)
    rep: Mapped[int] = mapped_column(Integer, nullable=False)
    sets: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    profile: Mapped["ExerciseProfileModel"] = relationship(  # noqa: F821, UP037
        back_populates="logs"
    )
