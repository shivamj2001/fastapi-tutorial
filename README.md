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

## Features Implemented So Far

- Full **CRUD API** for Users
- Clean **project structure** (routers, schemas, services, core)
- **Request & Response schema separation**
- **Service layer** for business logic
- **Request logging middleware**
- **Background audit task** (non-blocking)
- **Global error handling**
- Environment-based **configuration management**
- In-memory data store (for learning purpose)
## Project Structure

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



## Architecture Overview

Client
↓
Router (HTTP handling)
↓
Service (business logic)
↓
Schemas (validation & serialization)
↓
Response


## Request Logging Middleware

- A global middleware logs:

- HTTP method

- URL path

- Status code

- Time taken

- Example log:

- POST /users -> 200 [0.0123s]

This helps in debugging, monitoring, and auditing.

## CRUD APIs Implemented
- Operation	Endpoint
- Create user	POST /users
- Get all users	GET /users
- Get user by ID	GET /users/{id}
- Update user	PUT /users/{id}
- Delete user	DELETE /users/{id}


## Background Audit Task

- Important actions (like user creation) are logged in the background using FastAPI’s BackgroundTasks.

- Response is sent immediately

- Audit logging runs asynchronously

- Simulates DB/file/external logging

Example output:

[AUDIT] CREATE_USER | User 1 created

## Global Error Handling

- A global exception handler:

- Catches all unhandled exceptions

- Prevents stack traces from leaking

- Returns a clean error response

Example response:

{
  "success": false,
  "message": "Internal server error"
}
