# ParserHub

ParserHub is a platform for managing, scheduling, and running web parsers through a unified interface.

The project is designed as a modular platform where individual parsers can be developed and integrated without changing the core application.

ParserHub is also an educational and portfolio project focused on backend architecture, asynchronous programming, web parsing, distributed task processing, and scalable system design.

---

## Current Status

ParserHub is currently in **Stage 1 — Foundation**.

Implemented:

* layered backend architecture;
* FastAPI application;
* API versioning;
* PostgreSQL integration;
* asynchronous SQLAlchemy;
* Alembic migrations;
* user model;
* JWT authentication;
* password hashing;
* authentication dependencies;
* centralized error handling;
* backend tests;
* Ruff;
* mypy;
* pytest;
* pre-commit;
* GitHub Actions CI;
* Docker Compose development infrastructure.

Currently being completed:

* Next.js frontend;
* frontend/backend integration;
* dashboard;
* final Stage 1 integration.

The project roadmap is available in [`docs/roadmap.md`](docs/roadmap.md).

---

## Architecture

ParserHub follows a layered architecture.

The current backend structure is:

```text
Client
   │
   ▼
FastAPI API
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
PostgreSQL
```

The planned architecture extends this foundation with asynchronous task processing:

```text
Frontend
   │
   ▼
API
   │
   ▼
Services
   │
   ├───────────────┐
   ▼               ▼
Repositories    Task Queue
   │               │
   ▼               ▼
PostgreSQL       Workers
                   │
                   ▼
                Parsers
                   │
                   ▼
                Pipeline
                   │
                   ▼
               PostgreSQL
```

Parsers will implement a common interface and operate independently from the core application.

For detailed architectural decisions, see [`docs/architecture.md`](docs/architecture.md).

---

## Technology Stack

### Frontend

* Next.js
* TypeScript
* React
* Tailwind CSS
* TanStack Query
* shadcn/ui

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy 2
* Alembic
* Pydantic
* pydantic-settings
* PyJWT
* pwdlib + Argon2
* Uvicorn

### Database

* PostgreSQL

### Task Processing

* Redis
* Arq

### Parsing

* httpx
* Beautiful Soup
* lxml
* Playwright

### Development & Quality

* uv
* Ruff
* mypy
* pytest
* pre-commit

### Infrastructure

* Docker
* Docker Compose
* Nginx
* GitHub Actions

The complete stack is documented in [`docs/stack.md`](docs/stack.md).

---

## Quick Start

### Requirements

* Git
* Python 3.12
* uv
* Node.js
* Docker

### Clone the repository

```bash
git clone <repository-url>
cd parserhub
```

### Configure environment

Copy `.env.example` to `.env` and configure the required environment variables.

The `.env` file must not be committed to Git.

### Start PostgreSQL

From the repository root:

```bash
docker compose up -d
```

Check the container:

```bash
docker compose ps
```

### Setup the backend

```bash
cd backend
uv sync
```

Apply database migrations:

```bash
uv run alembic upgrade head
```

Start the development server:

```bash
uv run uvicorn parserhub.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI provides interactive API documentation at `/docs`.

For the complete development workflow, see [`docs/development.md`](docs/development.md).

---

## Project Structure

```text
parserhub/
│
├── .github/
│   └── workflows/
│
├── backend/
│   ├── src/
│   │   └── parserhub/
│   │       ├── api/
│   │       ├── core/
│   │       ├── db/
│   │       ├── models/
│   │       ├── repositories/
│   │       ├── schemas/
│   │       └── services/
│   │
│   ├── tests/
│   ├── alembic/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── parser-guidelines.md
│   ├── roadmap.md
│   ├── stack.md
│   └── vision.md
│
├── scripts/
│
├── compose.yaml
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
└── README.md
```

The project structure will evolve as new stages are implemented.

---

## Documentation

Detailed project documentation:

* [`Architecture`](docs/architecture.md) — system architecture and architectural decisions.
* [`Development`](docs/development.md) — development environment, workflow, tooling, testing, Docker, and Git conventions.
* [`Parser Guidelines`](docs/parser-guidelines.md) — rules and conventions for implementing parsers.
* [`Roadmap`](docs/roadmap.md) — project stages and planned development.
* [`Stack`](docs/stack.md) — technologies and infrastructure used by the project.
* [`Vision`](docs/vision.md) — long-term project vision and goals.

---

## Roadmap

ParserHub is being developed incrementally.

```text
Stage 0 — Planning
        │
        ▼
Stage 1 — Foundation
        │
        ▼
Stage 2 — Core Engine
        │
        ▼
Stage 3 — Task Queue
        │
        ▼
Stage 4 — Monitoring
        │
        ▼
Stage 5 — Dashboard
        │
        ▼
Stage 6 — Scheduler
        │
        ▼
Stage 7 — Data Pipeline
        │
        ▼
Stage 8 — WebSocket
        │
        ▼
Stage 9 — Plugin System
        │
        ▼
Stage 10 — Production
```

See [`docs/roadmap.md`](docs/roadmap.md) for details.

---

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## Disclaimer

ParserHub is an educational and demonstration project.

Parsers developed for the platform may interact with third-party websites. Users are responsible for complying with applicable laws, website terms of service, access restrictions, and `robots.txt` policies when creating and operating parsers.
