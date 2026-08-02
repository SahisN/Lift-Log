from datetime import date
from uuid import UUID

from sqlalchemy import Date, Float, ForeignKey, Integer, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExerciseProfileModel(Base):
    __tablename__ = "exercise_profiles"
    __table_args__ = (UniqueConstraint("user_id", "exercise_id"),)

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        index=True,
    )

    exercise_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("exercises.id"), index=True, nullable=False
    )

    current_weight: Mapped[float] = mapped_column(Float, nullable=False)
    current_reps: Mapped[int] = mapped_column(Integer, nullable=False)
    current_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    achieved_date: Mapped[date] = mapped_column(Date, nullable=False)

    exercise: Mapped["ExerciseModel"] = relationship(  # noqa: F821
        back_populates="exercise_profiles"
    )
    logs: Mapped[list["ExerciseLogModel"]] = relationship(  # noqa: F821
        back_populates="profile"
    )
