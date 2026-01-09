import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import Settings
from app.routers.users import router as users_router

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(users_router)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    print(
        f"{request.method} {request.url.path} "
        f"-> {response.status_code} "
        f"[{duration:.4f}s]"
    )

    return response

# Global exception handler to clearly handle error messages
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )
