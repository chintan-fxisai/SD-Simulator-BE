# Backend Development Context

## Project Overview

This is a backend application built using:

- FastAPI
- Python 3.12+
- SQLAlchemy 2.0 (Async)
- Alembic
- MySQL
- Pydantic v2
- JWT Authentication
- Docker (Optional)

The application should be scalable, maintainable, secure, and production-ready.

---

# Core Principles

Always follow:

- Clean code principles
- Service Layer Architecture
- Separation of concerns
- Type safety
- Async-first development
- Security best practices
- Reusable business logic
- Database transaction safety

Never:

- Put business logic inside routes
- Write raw SQL unless necessary
- Hardcode secrets
- Hardcode configuration values
- Duplicate business logic
- Use synchronous database operations
- Use global mutable state

---

# Project Structure

app/
│
├── api/
│   ├── endpoints/
│   └── dependencies/
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── exceptions.py
│   └── constants.py
│
├── db/
│   ├── session.py
│   ├── base.py
│   └── migrations/
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── permissions/
│
├── middleware/
│
├── utils/
│
├── workers/
│
└── main.py

---

# Architecture Rules

Request Flow:

Client
→ API Route
→ Service
→ Repository
→ Database

Response Flow:

Database
→ Repository
→ Service
→ API Route
→ Client

Routes must never directly access the database.

Bad:

```python
@router.post("/")
async def create_user():
    user = User(...)
    db.add(user)
```

Good:

```python
@router.post("/")
async def create_user():
    return await user_service.create_user(...)
```

---

# API Versioning

All APIs must be versioned.

Example:

/api/v1/auth/login
/api/v1/users
/api/v1/projects

Never expose unversioned APIs.

---

# Async Development

Use async everywhere.

Example:

```python
async def create_user():
```

Database sessions must be async.

Example:

```python
AsyncSession
```

Never use:

```python
Session
```

unless explicitly required.

---

# Database Rules

Database:

MySQL 

Encoding: 
utfmb4 

ORM:

SQLAlchemy 2.0 Async

Always:

- Use ORM models
- Use relationships properly
- Use indexes where needed
- Use foreign key constraints

Avoid:

- N+1 queries
- Unnecessary joins
- Loading excessive data

---

# Model Rules

Models should:

- Have timestamps
- Use UUIDs when appropriate
- Define relationships clearly

Example:

```python
created_at
updated_at
```

Prefer reusable base models.

---

# Schema Rules

Use Pydantic v2.

Create separate schemas:

Example:

```python
UserCreate
UserUpdate
UserResponse
```

Never expose database models directly.

---

# Repository Layer

Repositories handle:

- Database access
- Query construction
- Persistence operations

Repositories should not contain:

- Business rules
- Validation logic

Example:

```python
class UserRepository:
    async def get_by_email(...)
```

---

# Service Layer

Services handle:

- Business logic
- Validation
- Permission checks
- Workflow orchestration

Example:

```python
class UserService:
    async def create_user(...)
```

Services should not know HTTP details.

Avoid:

```python
raise HTTPException(...)
```

inside services.

Use custom exceptions.

---

# Authentication

Authentication Strategy:

JWT Access Token
+
JWT Refresh Token
+
Session Management

---

Access Token:

Short-lived

Example:

15 minutes

---

Refresh Token:

Long-lived

Example:

7 days

---

Store hashed refresh tokens.

Never store plain refresh tokens.

---

# Session Management

Maintain user sessions in database.

Example:

UserSession

- id
- user_id
- refresh_token_hash
- device_info
- ip_address
- user_agent
- created_at
- expires_at
- revoked_at

Features:

- Multi-device login
- Logout current session
- Logout all sessions
- Session tracking

---

# Security Rules

Always:

- Hash passwords using bcrypt
- Validate all input
- Use JWT signing secrets from env
- Use rate limiting where applicable
- Validate permissions
- Sanitize user input

Never:

- Store plain passwords
- Return sensitive fields
- Log secrets

---

# RBAC

Use normalized RBAC.

Tables:

Role
Permission
RolePermission
UserRole

Example:

Role:
- Super Admin
- Admin
- Manager
- User

Permission:

- user:create
- user:update
- user:view
- user:delete

Permission checks should be reusable.

Example:

```python
@require_permission("user:create")
```

Never hardcode role names in business logic.

Always check permissions.

---

# Error Handling

Create centralized exception handling.

Example:

```python
AppException
NotFoundException
ValidationException
PermissionDeniedException
```

Return consistent responses.

Example:

```json
{
  "success": false,
  "message": "User not found",
  "errors": []
}
```

---

# Response Format

Success:

```json
{
  "success": true,
  "message": "Operation completed",
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "message": "Something went wrong",
  "errors": []
}
```

Always keep response structure consistent.

---

# Pagination

List endpoints must support:

- page
- page_size

Return:

```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

---

# Filtering

Design APIs to support filtering.

Example:

```http
GET /users?status=active
```

---

# Sorting

Design APIs to support sorting.

Example:

```http
GET /users?sort_by=created_at&order=desc
```

---

# Configuration

Use environment variables as-
get all the variables in config.py file
use variables from config.py throughout the application.

Example:

DATABASE_URL=
JWT_SECRET=
JWT_REFRESH_SECRET=

Never hardcode configuration.

---

# Logging

Use structured logging.

Log:

- Requests
- Errors
- Security events

Do not log:

- Passwords
- Tokens
- Secrets

---

# Alembic

All schema changes must use Alembic migrations.

Never manually alter production schema.

---

# Docker

Docker support should be optional.

Application must run:

- Locally
- Dockerized

without code changes.

---

# Code Generation Instructions

When generating code:

1. Follow Service Layer Architecture.
2. Use FastAPI.
3. Use Async SQLAlchemy.
4. Use Pydantic v2.
5. Use Repository Pattern.
6. Keep business logic inside services.
7. Keep routes thin.
8. Use JWT + Session Management.
9. Use normalized RBAC.
10. Create reusable components.
11. Use production-ready patterns.
12. Follow security best practices.
13. Avoid temporary fixes and hacks.
14. Ensure scalability and maintainability.
15. Generate code compatible with existing architecture.