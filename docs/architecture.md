# Architecture

ParserHub is designed as a layered backend architecture with a clear separation between API, application logic, data access, and infrastructure.

The architecture is designed to support the future introduction of asynchronous task processing, workers, and a parser execution pipeline.

---

## Current Architecture

The current implementation contains the following main layers:

```text
                    ┌──────────────┐
                    │   Frontend   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  FastAPI API │
                    └──────┬───────┘
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
           Dependencies         Services
                  │                 │
                  │                 ▼
                  │          Repositories
                  │                 │
                  └────────┐        │
                           ▼        ▼
                         PostgreSQL
```

The current architecture focuses on establishing the application's foundation:

* versioned API;
* request and response validation;
* authentication;
* application services;
* repository-based database access;
* SQLAlchemy database layer;
* dependency injection;
* centralized exception handling;
* automated testing.

The parser execution pipeline and background workers are part of the target architecture and are implemented in later stages.

---

## Target Architecture

The target architecture extends the current backend with asynchronous task processing and parser execution.

```text
                              ┌──────────────┐
                              │   Frontend   │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │   API Layer  │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │Service Layer │
                              └──────┬───────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
             ┌──────────────┐                  ┌──────────────┐
             │ Repositories │                  │  Task Queue  │
             └──────┬───────┘                  └──────┬───────┘
                    │                                 │
                    ▼                                 ▼
             ┌──────────────┐                  ┌──────────────┐
             │ PostgreSQL   │                  │   Workers    │
             └──────────────┘                  └──────┬───────┘
                                                      │
                                                      ▼
                                               ┌──────────────┐
                                               │ Parser Engine│
                                               └──────┬───────┘
                                                      │
                                                      ▼
                                               ┌──────────────┐
                                               │   Pipeline   │
                                               └──────┬───────┘
                                                      │
                                                      ▼
                                               ┌──────────────┐
                                               │ PostgreSQL   │
                                               └──────────────┘
```

The target architecture separates HTTP request processing from long-running parser execution.

API requests should create and manage tasks rather than executing long-running parsers directly.

Workers are responsible for executing parser tasks outside the API process.

---

# Components

## Frontend

The frontend provides the user interface for interacting with ParserHub.

Responsibilities:

* user interface;
* authentication;
* dashboard;
* parser management;
* task management;
* displaying parser results.

Technology:

* Next.js;
* TypeScript.

The frontend is part of the target system and is not currently implemented in the repository.

---

## Backend API

The API layer is responsible for HTTP-specific concerns.

Responsibilities:

- HTTP requests;
- API routing;
- request validation;
- response serialization;
- authentication endpoints;
- dependency injection;
- mapping application results to API responses.

Technology:

- FastAPI.

The API is organized into a root router, operational endpoints, and versioned API routers.

Current implementation:

```text
backend/src/parserhub/api/

├── router.py
├── health.py
├── version.py
└── v1/
    ├── router.py
    └── endpoints/
        ├── auth.py
        └── users.py
```

The root API router is responsible for assembling the complete API.

Versioned application endpoints are mounted under /api/v1.

Operational endpoints such as /health and /version are kept outside the versioned API because they describe the availability and metadata of the running application rather than a versioned business API contract.

API endpoints should remain thin and should delegate application logic to services.

---

```markdown
## API Versioning

ParserHub uses explicit URL-based API versioning for application endpoints.

Current API version:

```text
/api/v1

The API routing hierarchy is:

api/router.py
    │
    ▼
/api/v1
    │
    ▼
api/v1/router.py
    │
    ├── /auth
    │
    └── /users
```

The versioned router is implemented in:


`backend/src/parserhub/api/v1/router.py`

The root API router is implemented in:

`backend/src/parserhub/api/router.py`

Endpoint implementations are located in:

`backend/src/parserhub/api/v1/endpoints/`

Current application endpoints include:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/users/me
```

Operational endpoints are intentionally kept outside the versioned API:

```text
GET /health
GET /version
```

Future breaking changes to the application API should be introduced through a new API version rather than silently changing the existing contract.

---

```markdown
## Operational Endpoints

ParserHub provides a small set of endpoints for application health and runtime metadata.

These endpoints are not part of the versioned application API.

### Health

```text
GET /health
```

The health endpoint verifies that the application process is available.

Implementation:

`backend/src/parserhub/api/health.py`

Schema:

`backend/src/parserhub/schemas/health.py`

Response:

```JSON
{
    "status": "ok"
}
```

### Version
```text
GET /version
```

The version endpoint exposes the current ParserHub application version and runtime environment.

Implementation:

`backend/src/parserhub/api/version.py`

Schema:

`backend/src/parserhub/schemas/version.py`

The application version is maintained as package metadata rather than duplicated in environment configuration.

Version-related functionality is implemented in:

`backend/src/parserhub/core/version.py`

---

## Service Layer

The service layer contains application and business logic.

Responsibilities include:

* user registration;
* authentication;
* parser execution;
* task creation;
* result processing;
* coordination between repositories and other application components.

Current implementation:

```text
backend/src/parserhub/services/
└── auth.py
```

Services should not contain HTTP-specific logic.

Services should also avoid depending directly on SQLAlchemy session implementation details.

---

## Repository Layer

The repository layer isolates data access from application logic.

Responsibilities:

* querying persistent data;
* creating records;
* updating records;
* deleting records;
* encapsulating database-specific operations.

Current implementation:

```text
backend/src/parserhub/repositories/
└── user.py
```

Repositories use the database layer to access PostgreSQL.

Application services interact with repositories rather than performing database queries directly.

---

## Database Layer

The database layer provides database connectivity and transaction management.

Current implementation:

```text
backend/src/parserhub/db/
├── base.py
├── session.py
└── unit_of_work.py
```

Responsibilities:

* SQLAlchemy configuration;
* asynchronous database sessions;
* transaction management;
* Unit of Work management;
* database connection lifecycle.

PostgreSQL is currently the primary persistent storage.

Database schema changes are managed through Alembic:

```text
backend/alembic/
├── env.py
└── versions/
```

---

## Models

SQLAlchemy models represent persistent database entities.

Current implementation:

```text
backend/src/parserhub/models/
├── enums.py
└── user.py
```

Models are used for database persistence and must not be used directly as API contracts.

API input and output contracts are defined using Pydantic schemas.

---

## Schemas

Pydantic schemas define API data contracts.

Current implementation:

```text
backend/src/parserhub/schemas/

├── auth.py
├── error.py
├── health.py
├── user.py
└── version.py
```

Schemas are responsible for:

request validation;
response serialization;
defining API contracts;
separating external API data from internal database models.

---

## Dependencies

FastAPI dependencies provide request-scoped application dependencies.

Current implementation:

```text
backend/src/parserhub/core/dependencies.py
```

Dependencies are used to provide components such as:

* database access;
* authenticated user context;
* other request-scoped dependencies.

Dependencies are not a business-logic layer.

They connect the HTTP layer with application and infrastructure components.

---

## Core

The `core` package contains cross-cutting application infrastructure and configuration.

Current implementation:

```text
backend/src/parserhub/core/

├── config.py
├── constants.py
├── dependencies.py
├── exceptions.py
├── exception_handlers.py
├── security.py
└── version.py
```

Responsibilities include:

application configuration;
application version information;
security utilities;
authentication dependencies;
application exceptions;
exception handling;
shared constants.

---

# Authentication Architecture

Authentication is implemented as a cross-cutting backend feature using the API, service, repository, security, and dependency layers.

The authentication flow consists of:

```text
API Endpoint
     │
     ▼
AuthService
     │
     ▼
UserRepository
     │
     ▼
PostgreSQL
```

Authentication uses:

* password hashing;
* password verification;
* JWT access tokens;
* authentication dependencies;
* centralized authentication errors.

Relevant implementation:

```text
backend/src/parserhub/
├── api/v1/endpoints/auth.py
├── api/v1/endpoints/users.py
├── services/auth.py
├── repositories/user.py
├── core/security.py
├── core/dependencies.py
├── core/exceptions.py
├── core/exception_handlers.py
├── models/user.py
└── schemas/
    ├── auth.py
    └── user.py
```

---

## Login Flow

```text
POST /api/v1/auth/login
            │
            ▼
       Auth Endpoint
            │
            ▼
        AuthService
            │
            ▼
       UserRepository
            │
            ▼
        PostgreSQL
            │
            ▼
    Password Verification
            │
            ▼
   create_access_token()
            │
            ▼
           JWT
            │
            ▼
          Client
```

The API endpoint is responsible for HTTP concerns.

The service coordinates the authentication process.

The repository retrieves the user from the database.

Password verification and JWT handling are isolated in the security layer.

---

## Authenticated Request Flow

Protected endpoints use an authentication dependency to obtain the current authenticated user.

```text
GET /api/v1/users/me
            │
            ▼
    get_current_user()
            │
            ▼
   Decode JWT Access Token
            │
            ▼
       UserRepository
            │
            ▼
        PostgreSQL
            │
            ▼
     Current User
            │
            ▼
         Endpoint
            │
            ▼
        API Response
```

Authentication dependencies are implemented in:

```text
backend/src/parserhub/core/dependencies.py
```

Security-related functionality is implemented in:

```text
backend/src/parserhub/core/security.py
```

---

# Exception Handling

ParserHub uses centralized exception handling for application-level errors.

Current implementation:

```text
backend/src/parserhub/core/
├── exceptions.py
└── exception_handlers.py
```

The purpose of centralized exception handling is to keep error processing consistent across API endpoints.

API endpoints should not duplicate application-wide exception handling logic.

Error response schemas are defined in:

```text
backend/src/parserhub/schemas/error.py
```

---

# Parser Engine

The Parser Engine is responsible for executing parsers and managing their lifecycle.

Responsibilities:

* parser discovery;
* parser registration;
* parser lifecycle;
* parser execution;
* parser result handling.

The Parser Engine is part of the target architecture and is not yet implemented in the current backend.

Parser implementations will follow the common `BaseParser` interface defined by the project.

Parser-specific development rules are documented in:

```text
docs/parser-guidelines.md
```

---

# Workers

Workers are responsible for executing long-running background operations outside the API process.

Responsibilities:

* consuming parser tasks;
* executing parser jobs;
* handling long-running operations;
* reporting task status;
* storing parser results.

Workers are part of the target architecture and will be implemented in later stages.

The API should not execute long-running parser operations directly.

---

# Task Queue

The task queue decouples API requests from parser execution.

The expected flow is:

```text
API
 │
 ▼
Create Task
 │
 ▼
Task Queue
 │
 ▼
Worker
 │
 ▼
Parser
```

This allows parser execution to happen asynchronously and independently from the API process.

The concrete task queue technology will be selected and implemented in a later stage.

---

# Parser Pipeline

The parser pipeline represents the processing flow from a parser task to persisted results.

```text
Task
 │
 ▼
Worker
 │
 ▼
Parser
 │
 ▼
Raw Data
 │
 ▼
Validation / Transformation
 │
 ▼
Normalized Result
 │
 ▼
PostgreSQL
```

The pipeline is part of the target architecture and will be expanded as parser functionality is implemented.

---

# Data Flow

## Authentication

```text
Client
  │
  ▼
API
  │
  ▼
AuthService
  │
  ▼
UserRepository
  │
  ▼
PostgreSQL
```

## Parser Execution

The target parser execution flow is:

```text
Client
  │
  ▼
API
  │
  ▼
Task
  │
  ▼
Task Queue
  │
  ▼
Worker
  │
  ▼
Parser
  │
  ▼
Pipeline
  │
  ▼
PostgreSQL
  │
  ▼
API
  │
  ▼
Client
```

---

# Architectural Rules

The following rules define the main architectural boundaries of ParserHub.

1. API endpoints must contain HTTP-specific logic only.

2. API endpoints must not contain business logic.

3. Services contain application and business logic.

4. Services should not depend directly on HTTP-specific details.

5. Database access must be handled through repositories.

6. Services should not depend directly on SQLAlchemy session implementation details.

7. Pydantic schemas define API input and output contracts.

8. SQLAlchemy models represent persistent database entities and must not be used directly as API contracts.

9. Authentication dependencies provide authenticated user context to API endpoints.

10. Password hashing and JWT handling must remain isolated from API endpoints.

11. Infrastructure-specific code should remain isolated from application logic where practical.

12. Long-running parser operations must not be executed directly inside API request handlers.

13. Parsers must implement the common `BaseParser` interface.

14. Dependencies should flow from higher-level application logic toward lower-level infrastructure.

---

# Dependency Direction

The intended dependency direction is:

```text
API
 │
 ▼
Services
 │
 ▼
Repositories
 │
 ▼
Database / Infrastructure
```

Cross-cutting infrastructure such as configuration, security, and dependency injection supports the application without becoming part of the business logic.

The architecture should avoid dependencies flowing in the opposite direction.

For example:

```text
API → Service        Allowed
Service → Repository Allowed
Repository → DB      Allowed

Repository → API     Not allowed
Service → FastAPI    Not allowed
Model → API Schema   Not allowed
```

---

## Testing Architecture

Tests are organized according to the architectural boundaries they validate.

Current structure:

```text
backend/tests/

├── factories/
│   └── user.py
│
├── integration/
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       ├── test_auth.py
│   │   │       └── test_users.py
│   │   ├── test_health.py
│   │   └── test_version.py
│   ├── db/
│   │   ├── test_database.py
│   │   └── test_unit_of_work.py
│   ├── repositories/
│   │   └── test_user.py
│   └── services/
│       └── test_auth.py
│
├── unit/
│   ├── core/
│   │   ├── test_config.py
│   │   ├── test_dependencies.py
│   │   ├── test_exception_handlers.py
│   │   ├── test_security.py
│   │   └── test_version.py
│   └── services/
│       └── test_auth.py
│
└── conftest.py
```

Unit tests validate components in isolation.

Integration tests validate interactions between components and external infrastructure such as PostgreSQL.

API integration tests are organized according to the API structure they validate.

---

# Architecture Evolution

ParserHub is developed incrementally.

The current architecture represents the implemented foundation.

The target architecture represents the intended system after the introduction of:

* task processing;
* background workers;
* parser execution;
* parser pipelines;
* asynchronous task management;
* scalable parser execution.

Architectural decisions should be updated in this document when the implementation evolves.

The roadmap for planned architectural changes is documented in:

```text
docs/roadmap.md
```
