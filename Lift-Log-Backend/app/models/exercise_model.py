from uuid import UUID

from base import Base
from sqlalchemy import Boolean, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class ExerciseModel(Base):
    __tablename__ = "exercises"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    exercise_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    muscle_group: Mapped[str] = mapped_column(String, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String, nullable=False, index=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)
