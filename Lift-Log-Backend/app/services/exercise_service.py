from errors.errors import ExerciseNotFound
from models.exercise_model import ExerciseModel
from models.ids import ExerciseId
from repos.deps.wiring import ExerciseRepo
from schemas.exercise_schema import CreateExerciseRequest

from services.pagination_service import PaginatedData, PaginationService


class ExerciseService:
    def __init__(self, repo: ExerciseRepo, pagination: PaginationService):
        self._repo = repo
        self._pagination = pagination

    async def create_exercise(self, payload: CreateExerciseRequest) -> ExerciseModel:

        exercise = ExerciseModel(**payload.model_dump())
        return await self._repo.save(exercise)

    async def get_exercise(self, exercise_id: ExerciseId) -> ExerciseModel:
        exercise = await self._repo.get(exercise_id)
        if not exercise:
            raise ExerciseNotFound()
        return exercise

    async def list_exercise(self, page: int = 1, page_size: int = 100) -> PaginatedData:
        offset = (page - 1) * page_size
        items = await self._repo.list(limit=page_size, offset=offset)
        total = await self._repo.count()

        return self._pagination.paginate_list(items, page, page_size, total)
