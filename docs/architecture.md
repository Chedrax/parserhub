
# Architecture


## Overview

```
ParserHub follows layered architecture.

Frontend
    |
    |
API Layer
    |
    |
Service Layer
    |
    |
Repository Layer
    |
    |
Database
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
