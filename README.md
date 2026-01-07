main.py : starts the app
routes/ : API endpoints (APIRouter)
models.py : request body schemas (pydantic)

routes/user.py : routes + logic

app/main.py : 
FastAPI() : cretes app
include_router() : attaches user APIs (route registration)

app/models.py : 
UserCreate : used when creating/updating a user
User : what API returns (includes id)


config.py : application configuration (env-based)
.env      : environment variables
