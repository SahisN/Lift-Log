from errors.errors import ExerciseProfileNotFound
from models.exercise_profile_model import ExerciseProfileModel
from models.ids import ProfileId, UserId
from repos.exercise_profile_repo import ExerciseProfileRepo
from schemas.exercise_profile_schema import CreateExerciseProfileRequest

from services.pagination_service import PaginatedData, PaginationService


class ExerciseProfileService:
    def __init__(self, repo: ExerciseProfileRepo, pagination: PaginationService):
        self._repo = repo
        self._pagination = pagination

    async def get_exercise_profile(
        self, profile_id: ProfileId, user_id: UserId
    ) -> ExerciseProfileModel:
        exercise_profile = await self._repo.get(profile_id)
        if not exercise_profile or exercise_profile.user_id != user_id.value:
            raise ExerciseProfileNotFound
        return exercise_profile

    async def create_exercise_profile(
        self, payload: CreateExerciseProfileRequest
    ) -> ExerciseProfileModel:
        exercise_profile = ExerciseProfileModel(**payload.model_dump())
        return await self._repo.save(exercise_profile=exercise_profile)

    async def list_exercise_profile(
        self, user_id: UserId, page: int = 1, page_size: int = 100
    ) -> PaginatedData:
        total = await self._repo.count(user_id=user_id)
        if total <= 0:
            return self._pagination.paginate_list([], page, page_size, total)

        offset = (page - 1) * page_size
        items = await self._repo.list(user_id=user_id, limit=page_size, offset=offset)

        return self._pagination.paginate_list(items, page, page_size, total)
