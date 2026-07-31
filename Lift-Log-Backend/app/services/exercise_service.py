from errors.errors import ExerciseNotFound
from models.exercise_model import ExerciseModel
from models.ids import ExerciseId
from repo.deps.wiring import ExerciseRepo
from schemas.exercise_schema import CreateExerciseRequest


class ExerciseService:
    def __init__(self, repo: ExerciseRepo):
        self._repo = repo

    async def create_execrise(self, payload: CreateExerciseRequest) -> ExerciseModel:

        exercise = ExerciseModel(**payload.model_dump())
        return await self._repo.save(exercise)

    async def get_execrise(self, execrise_id: ExerciseId) -> ExerciseModel:
        execrise = await self._repo.get(execrise_id)
        if not execrise:
            raise ExerciseNotFound()
        return execrise

    async def list_execrise(
        self, limit: int = 100, offset: int = 0
    ) -> list[ExerciseRepo]:
        return await self._repo.list(limit=limit, offset=offset)
