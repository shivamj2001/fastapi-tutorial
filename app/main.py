import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import Settings
from app.routers.users import router as users_router
# Import the authentication router
from app.routers.auth import router as auth_router


# 1. Initialize settings to get app name and debug mode
settings = Settings()

# 2. Create the core FastAPI application instance
app = FastAPI(
    title=settings.app_name, # Sets the title shown in /docs
    debug=settings.debug     # If True, shows detailed error pages to the developer
)

# 3. Connect the user-related routes (GET, POST, etc.) to the main app
# This keeps the code organized by separating 'users' logic from 'main' logic.
app.include_router(users_router)
# 4. Connect the authentication-related routes to the main app
app.include_router(auth_router)


# --- MIDDLEWARE: The "Monitor" ---
# This function intercepts every single request coming into the server.
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    # A. Record the exact time a request arrives
    start_time = time.time()

    # B. Send the request to the actual route (e.g., /users) and wait for response
    response = await call_next(request)

    # C. Calculate how many seconds it took to process
    duration = time.time() - start_time

    # D. Log the details to the console/Terminal (Method, Path, Status Code, and Time)
    # Example: GET /users -> 200 [0.0045s]
    print(
        f"{request.method} {request.url.path} "
        f"-> {response.status_code} "
        f"[{duration:.4f}s]"
    )

    return response

# --- EXCEPTION HANDLER: The "Safety Net" ---
# If any code in your app crashes (like a DB error), this function catches it.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the real error to the server console so developers can see it
    print(f"Unhandled error: {exc}")

    # Return a clean, polite JSON message to the user 
    # This prevents the user from seeing messy "traceback" code.
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )