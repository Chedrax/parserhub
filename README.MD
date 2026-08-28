# ParserHub

ParserHub is a platform for managing, scheduling, and running web parsers through a unified interface.

The project is designed as a modular backend platform where individual parsers can be added without changing the core application.

## Overview

ParserHub is an educational and portfolio project focused on designing a modern parsing platform.

The project explores:

* layered backend architecture;
* asynchronous programming;
* task queues and background workers;
* parser abstraction and discovery;
* data processing pipelines;
* API design;
* database design;
* containerization;
* automated code quality checks;
* CI/CD;
* production deployment.

The architecture is designed to allow the platform to evolve from a local development environment into a scalable distributed system.

## Current Status

The project is currently in the **Foundation** stage.

Implemented:

* project structure;
* FastAPI backend foundation;
* `uv` dependency management;
* Ruff linting and formatting;
* mypy static type checking;
* pytest test framework;
* pre-commit hooks;
* GitHub Actions CI;
* development documentation.

Currently under development:

* Next.js frontend foundation;
* PostgreSQL integration foundation;
* user authentication;
* database models;
* API structure;
* frontend dashboard.

## Planned Features

The following functionality is planned for future stages:

* parser registry;
* common `BaseParser` interface;
* parser management;
* asynchronous task execution;
* Redis;
* Arq workers;
* task monitoring;
* parser progress tracking;
* scheduler;
* result storage;
* data normalization;
* WebSocket-based real-time updates;
* plugin system;
* production deployment;
* monitoring and observability.

## Architecture

The planned high-level architecture is:

```text
Frontend
   │
   ▼
FastAPI
   │
   ▼
Service Layer
   │
   ▼
Task Queue
   │
   ▼
Workers
   │
   ▼
Parsers
   │
   ▼
PostgreSQL
```

The architecture follows a layered approach with clear separation between API, application logic, data access, and infrastructure.

Parsers are designed as independent modules implementing a common interface.

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
* Uvicorn

### Database

* PostgreSQL

### Task Processing

* Redis
* Arq

### Parsing

* httpx
* Beautiful Soup / lxml
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

## Project Structure

```text
parserhub/

├── .github/
│   └── workflows/
│
├── backend/
│   ├── src/
│   │   └── parserhub/
│   ├── tests/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── README.md
│
├── frontend/
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
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
└── README.md
```

## Development

### Requirements

The following tools are required for local development:

* Git
* Python 3.12
* uv
* Node.js
* Docker

Backend dependencies are managed exclusively through `uv`.

### Backend Setup

Clone the repository and install backend dependencies:

```bash
git clone <repository-url>
cd parserhub/backend
uv sync
```

Install the pre-commit hooks:

```bash
uv run pre-commit install
```

Run backend checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest
```

More detailed development rules are available in [`docs/development.md`](docs/development.md).

## Documentation

Project documentation is located in the [`docs/`](docs/) directory.

* [Architecture](docs/architecture.md)
* [Development](docs/development.md)
* [Parser Guidelines](docs/parser-guidelines.md)
* [Roadmap](docs/roadmap.md)
* [Stack](docs/stack.md)
* [Vision](docs/vision.md)

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

## Disclaimer

ParserHub is an educational and demonstration project.

Parsers developed for the platform may interact with third-party websites. Users are responsible for complying with applicable laws, website terms of service, access restrictions, and `robots.txt` policies when creating and operating parsers.
