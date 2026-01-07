from fastapi import FastAPI
from core.config import Settings
from routers.users import router as users_router

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(users_router)


