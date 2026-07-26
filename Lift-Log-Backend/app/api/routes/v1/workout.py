from api.routes.routers import workout_router


@workout_router.get("/workouts", status_code=200)
async def get_workouts():
    return {"test": "work"}
