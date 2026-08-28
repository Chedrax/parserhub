
# Architecture


## Current architecture

```
Frontend
   │
   ▼
FastAPI
   │
   ▼
Application
   │
   ▼
Database
```

## Target architecture

```
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

---

# Components

## Frontend

Responsible for:

* user interface;
* dashboard;
* displaying tasks;
* managing parsers.

Technology:

* Next.js
* TypeScript

---

## Backend API

Responsible for:

* HTTP requests;
* authentication;
* validation;
* API responses.

Technology:

* FastAPI

---

## Service Layer

Contains business logic.

Examples:

* starting parser;
* creating tasks;
* processing results.

---

## Repository Layer

Responsible for database communication.

Rules:

Services never access database directly.

---

## Parser Engine

Responsible for:

* parser lifecycle;
* parser discovery;
* execution.

---

## Workers

Responsible for:

* background tasks;
* long-running operations.

---

## Data Flow

Example:

User clicks "Run parser"

```
Frontend

↓

API

↓

Task created

↓

Queue

↓

Worker

↓

Parser

↓

Database

↓

Frontend update
