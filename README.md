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


## 📁 Project Structure

app/
│
├── main.py # Application entry point
│
├── routers/
│ └── users.py # User CRUD API endpoints
│
├── schemas/
│ ├── init.py
│ ├── user_request.py # Request models (input)
│ ├── user_response.py # Response models (output)
│ └── common.py # Shared schemas
│
├── services/
│ ├── user_service.py # Business logic
│ └── audit_service.py # Background audit logging
│
├── core/
│ └── config.py # Application configuration
│
└── init.py