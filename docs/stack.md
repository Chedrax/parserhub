# Technology Stack

This document describes the technologies used by ParserHub and the technologies planned for future stages.

Technologies are divided into currently implemented and planned components where appropriate.

---

## Frontend

### Planned

* Next.js
* React
* TypeScript
* Tailwind CSS
* TanStack Query
* shadcn/ui

The frontend is part of the target architecture and will be implemented in a later stage.

---

## Backend

### Implemented

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy 2
* Alembic
* Pydantic
* pydantic-settings
* asyncpg

### Authentication

* PyJWT
* pwdlib
* Argon2

FastAPI is used as the backend web framework.

SQLAlchemy provides asynchronous database access through `AsyncEngine` and `AsyncSession`.

Alembic is used for database schema migrations.

Pydantic is used for request and response validation.

pydantic-settings is used for application configuration loaded from environment variables.

`asyncpg` is used as the asynchronous PostgreSQL driver.

PyJWT is used for JWT access token handling.

`pwdlib` with Argon2 is used for secure password hashing and verification.

---

## Database

### Implemented

* PostgreSQL 17

PostgreSQL is the primary persistent database.

The local development database is provided through Docker Compose.

---

## Queue

### Planned

* Redis
* Arq

Redis and Arq are planned for asynchronous task processing and background parser execution.

They are not currently part of the implemented backend.

---

## Scheduler

### Planned

* APScheduler

APScheduler is planned for scheduled parser execution and recurring tasks.

It is not currently part of the implemented backend.

---

## Parsing

### Planned

* httpx
* BeautifulSoup
* lxml
* Playwright

These technologies are planned for parser implementation.

Their usage may vary depending on the target website and parser requirements.

---

## Infrastructure

### Implemented

* Docker
* Docker Compose

Docker is currently used to provide local infrastructure, including PostgreSQL.

### Planned

* Nginx

Nginx is planned as part of the future production infrastructure.

---

## Testing

### Implemented

* pytest
* pytest-asyncio
* httpx

`pytest` is used as the primary testing framework.

`pytest-asyncio` provides support for asynchronous tests.

`httpx2` is used for HTTP client functionality in API tests.

---

## Code Quality

### Implemented

* Ruff
* mypy
* pre-commit

Ruff is used for linting and code formatting.

mypy is used for static type checking.

pre-commit is used for local automated Git checks.

---

## CI/CD

### Implemented

* GitHub Actions

GitHub Actions runs the project's automated backend checks in CI.

---

## Package & Environment Management

### Implemented

* uv

`uv` is used for Python dependency management, virtual environment management, and running backend development tools.

Backend dependencies are defined in:

```text
backend/pyproject.toml
```

Locked dependency versions are stored in:

```text
backend/uv.lock
```

---

## Technology Status

The current implementation is focused on establishing the backend foundation.

### Currently implemented

```text
Python
FastAPI
Uvicorn
SQLAlchemy
Alembic
Pydantic
pydantic-settings
asyncpg
PostgreSQL
PyJWT
pwdlib + Argon2
pytest
pytest-asyncio
httpx2
Ruff
mypy
pre-commit
uv
Docker
Docker Compose
GitHub Actions
```

### Planned

```text
Next.js
React
TypeScript
Tailwind CSS
TanStack Query
shadcn/ui

Redis
Arq
APScheduler

httpx
BeautifulSoup
lxml
Playwright

Nginx
```

The planned technologies may be adjusted as the architecture evolves.
