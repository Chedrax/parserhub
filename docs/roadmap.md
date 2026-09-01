# Roadmap

ParserHub is developed incrementally in stages.

The roadmap describes the planned evolution of the project from the initial foundation to a production-ready parser management platform.

---

## Stage 0 — Planning

**Status: Completed**

### Goal

Create the initial project documentation, architecture, development rules, and technical foundation.

### Completed

* Project vision
* Initial architecture
* Technology stack
* Development guidelines
* Parser guidelines
* Project roadmap
* Repository structure
* Git conventions
* Initial project configuration

---

## Stage 1 — Foundation

**Status: In Progress**

### Goal

Create a professional application foundation for ParserHub.

After completing Stage 1, the project should have a working web application skeleton with:

* backend;
* frontend;
* PostgreSQL;
* database migrations;
* authentication;
* Docker-based local infrastructure;
* automated tests;
* code quality checks;
* CI.

---

### 1.1 Backend Structure

**Status: Completed**

* [x] Layered backend structure
* [x] API layer
* [x] Core layer
* [x] Database layer
* [x] Models
* [x] Schemas
* [x] Repositories
* [x] Services
* [x] Utilities structure
* [x] Application entry point

---

### 1.2 Configuration

**Status: Completed**

* [x] `pydantic-settings`
* [x] Environment-based configuration
* [x] `.env`
* [x] `.env.example`
* [x] Environment validation
* [x] Development environment configuration
* [x] Production environment configuration

---

### 1.3 Database

**Status: Completed**

* [x] PostgreSQL
* [x] Docker Compose PostgreSQL
* [x] SQLAlchemy 2
* [x] AsyncEngine
* [x] AsyncSession
* [x] Session factory
* [x] Database dependency
* [x] Unit of Work
* [x] Database integration tests

---

### 1.4 Database Migrations

**Status: Completed**

* [x] Alembic
* [x] Alembic configuration
* [x] SQLAlchemy metadata integration
* [x] Initial migration
* [x] Users table migration
* [x] Migration testing

---

### 1.5 API Foundation

**Status: Completed**

* [x] FastAPI application
* [x] API versioning
* [x] `/api/v1` router
* [x] Health endpoint
* [x] Request schemas
* [x] Response schemas
* [x] Dependency injection
* [x] HTTP status code strategy
* [x] Centralized exception handling
* [x] Error response schemas

---

### 1.6 User Model

**Status: Completed**

* [x] User SQLAlchemy model
* [x] User repository
* [x] User schema
* [x] Email uniqueness
* [x] Password hash storage
* [x] User timestamps
* [x] Database migration
* [x] Repository tests

---

### 1.7 Authentication

**Status: Completed**

* [x] User registration
* [x] Login
* [x] Password hashing
* [x] Password verification
* [x] JWT access tokens
* [x] Access token validation
* [x] Authentication dependency
* [x] Current authenticated user
* [x] Authentication exceptions
* [x] Authentication error handling
* [x] Authentication tests
* [x] `/users/me`

Authentication is implemented using the following components:

```text
API
 ↓
AuthService
 ↓
UserRepository
 ↓
PostgreSQL
```

JWT and password hashing are isolated in the security layer.

---

### 1.8 Docker & Local Infrastructure

**Status: In Progress**

* [x] Docker Compose configuration
* [x] PostgreSQL container
* [x] PostgreSQL persistent volume
* [x] PostgreSQL healthcheck
* [x] Environment-based database configuration
* [x] Docker development documentation

Remaining:

* [ ] Containerized backend
* [ ] Backend ↔ PostgreSQL Docker networking
* [ ] Full `docker compose up` application startup

The current Docker setup is primarily used to provide PostgreSQL for local development.

---

### 1.9 Testing

**Status: In Progress**

* [x] pytest
* [x] pytest-asyncio
* [x] Unit tests
* [x] Integration tests
* [x] Configuration tests
* [x] Security tests
* [x] Dependency tests
* [x] Exception handler tests
* [x] Authentication tests
* [x] Repository tests
* [x] Unit of Work tests
* [x] Database tests
* [x] API tests

Remaining:

* [ ] Complete final integration test coverage for Stage 1
* [ ] Frontend tests

---

### 1.10 Code Quality & Development Tooling

**Status: Completed**

* [x] Ruff
* [x] Ruff formatter
* [x] mypy
* [x] pre-commit
* [x] Conventional Commit validation
* [x] `uv` dependency management
* [x] Locked dependencies with `uv.lock`

---

### 1.11 CI

**Status: Completed**

* [x] GitHub Actions workflow
* [x] Python environment setup
* [x] Dependency installation with `uv`
* [x] Ruff linting
* [x] Ruff formatting check
* [x] mypy
* [x] pytest

CI validates backend changes independently of local pre-commit hooks.

---

### 1.12 Frontend

**Status: Not Started**

* [ ] Next.js application
* [ ] TypeScript
* [ ] React
* [ ] Tailwind CSS
* [ ] TanStack Query
* [ ] shadcn/ui
* [ ] API client
* [ ] Authentication UI
* [ ] Dashboard
* [ ] Backend API integration

---

### 1.13 CORS

**Status: Not Started**

* [ ] FastAPI CORS configuration
* [ ] Development frontend origin
* [ ] Production frontend origin configuration

CORS should be configured through environment-specific settings and should not rely on unrestricted wildcard origins in production.

---

### 1.14 Health & Version

**Status: Partially Completed**

* [x] `/health`
* [ ] `/version`

The health endpoint provides a simple application health check.

A version endpoint may be added before the final Stage 1 integration if it provides value for deployment and diagnostics.

---

### 1.15 Final Integration

**Status: Not Started**

Verify the complete application flow:

```text
Browser
   │
   ▼
Next.js
   │
   ▼
FastAPI
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

The final Stage 1 application should allow a user to:

1. Open the frontend.
2. Register an account.
3. Log in.
4. Receive an access token.
5. Make authenticated API requests.
6. Retrieve the current user.
7. Open the dashboard.

---

## Stage 1 — Definition of Done

Stage 1 is complete when:

```text
[ ] Backend foundation is complete
[x] Configuration is implemented
[x] PostgreSQL works locally
[x] Async SQLAlchemy is configured
[x] Alembic migrations work
[x] User model exists
[x] User repository exists
[x] Authentication works
[x] JWT authentication works
[x] Current user dependency works
[x] API versioning works
[x] Error handling is centralized
[x] Backend tests pass
[x] Ruff passes
[x] mypy passes
[x] pre-commit passes
[x] CI passes

[ ] Frontend is implemented
[ ] Frontend communicates with the backend
[ ] Authentication works through the frontend
[ ] Dashboard exists
[ ] CORS is configured
[ ] Final integration is complete
[ ] Docker runs the complete local application
[ ] Documentation is updated
```

When all required items are complete, Stage 1 is considered finished.

The next stage is:

---

## Stage 2 — Core Parser Engine

### Goal

Create the core abstraction for parser development and execution.

### Planned

* [ ] `BaseParser`
* [ ] Parser interface
* [ ] Parser lifecycle
* [ ] Parser configuration
* [ ] Parser Registry
* [ ] Parser Manager
* [ ] Parser discovery
* [ ] Parser execution abstraction
* [ ] Parser-specific tests

---

## Stage 3 — Task Queue

### Goal

Move long-running parser execution outside the API process.

### Planned

* [ ] Redis
* [ ] Arq
* [ ] Task model
* [ ] Task lifecycle
* [ ] Worker process
* [ ] Task queue integration
* [ ] Parser task execution
* [ ] Failed task handling
* [ ] Retry mechanism

---

## Stage 4 — Monitoring

### Goal

Provide visibility into parser and task execution.

### Planned

* [ ] Task status tracking
* [ ] Parser execution progress
* [ ] Structured logging
* [ ] Error tracking
* [ ] Application metrics
* [ ] Worker monitoring

---

## Stage 5 — Dashboard

### Goal

Create the web interface for managing ParserHub.

### Planned

* [ ] Next.js application
* [ ] TypeScript
* [ ] Authentication UI
* [ ] Dashboard
* [ ] Parser management
* [ ] Task management
* [ ] Result viewing
* [ ] API integration

---

## Stage 6 — Scheduler

### Goal

Support automatic and recurring parser execution.

### Planned

* [ ] APScheduler
* [ ] Scheduled parser tasks
* [ ] Recurring execution
* [ ] Schedule management
* [ ] Schedule persistence
* [ ] Failure handling

---

## Stage 7 — Data Pipeline

### Goal

Create a consistent pipeline for processing parser output.

### Planned

* [ ] Raw parser results
* [ ] Validation
* [ ] Data normalization
* [ ] Transformation
* [ ] Result persistence
* [ ] Common data models
* [ ] Pipeline error handling

---

## Stage 8 — Realtime Updates

### Goal

Provide realtime information about parser and task execution.

### Planned

* [ ] WebSocket API
* [ ] Task status updates
* [ ] Parser progress updates
* [ ] Dashboard realtime integration

---

## Stage 9 — Parser Extension System

### Goal

Create a controlled mechanism for extending ParserHub with additional parsers.

### Planned

* [ ] Parser registration system
* [ ] Parser metadata
* [ ] Parser configuration
* [ ] Parser lifecycle management
* [ ] Parser isolation
* [ ] Extension architecture

ParserHub should not allow arbitrary Python code or untrusted Python plugins to be uploaded and executed through the web interface.

Parser extensions must follow the project's parser architecture and security boundaries.

---

## Stage 10 — Production

### Goal

Prepare ParserHub for production deployment and scaling.

### Planned

* [ ] Production Docker configuration
* [ ] Nginx
* [ ] Production configuration
* [ ] Deployment automation
* [ ] Database backups
* [ ] Monitoring
* [ ] Logging
* [ ] Security hardening
* [ ] Horizontal scaling
* [ ] Worker scaling
* [ ] Production CI/CD

---

## Roadmap Status

The current development focus is:

```text
Stage 1 — Foundation
        │
        ├── 1.1 Project Foundation      ✓
        ├── 1.2 Configuration           ✓
        ├── 1.3 Database                ✓
        ├── 1.4 Database Migrations     ✓
        ├── 1.5 API Foundation          ✓
        ├── 1.6 Authentication          ✓
        ├── 1.7 CI                     ✓
        └── 1.8 Remaining Foundation    →
```

After Stage 1 is completed, development will continue with:

```text
Stage 2
Core Parser Engine
        ↓
Stage 3
Task Queue & Workers
        ↓
Stage 4
Monitoring
        ↓
Stage 5
Dashboard
        ↓
Stage 6
Scheduler
        ↓
Stage 7
Data Pipeline
        ↓
Stage 8
Realtime Updates
        ↓
Stage 9
Parser Extension System
        ↓
Stage 10
Production
```

The roadmap is subject to change as architectural and technical requirements evolve.
