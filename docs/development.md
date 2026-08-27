# Development Rules

This document defines the development conventions and workflow used in the ParserHub project.

The goal is to keep the codebase consistent, maintainable, and easy to work with as the project grows.


## Architecture Rules

ParserHub follows a layered architecture.

1. API layer is responsible for HTTP concerns only.
2. API layer must not contain business logic.
3. Services contain application and business logic.
4. Database access must be handled through repositories.
5. Services should not depend directly on SQLAlchemy session implementation details.
6. Pydantic schemas are used for API input and output validation.
7. SQLAlchemy models represent database entities and must not be used directly as API contracts.
8. Parsers must implement the common `BaseParser` interface.
9. Infrastructure-specific code should remain isolated from the domain and application logic.
10. Dependencies should flow from higher-level application logic toward lower-level infrastructure.


## Python Code Style

The backend targets Python 3.12.

Use modern Python syntax where possible.

### Type Hints

Prefer built-in generic types:

```python
list[str]
dict[str, int]
tuple[int, str]
set[str]
````

Prefer the union operator:

```python
str | None
str | int
```

Avoid legacy typing aliases when an equivalent modern syntax is available:

```python
# Preferred
users: list[str]
username: str | None

# Avoid
from typing import List, Optional

users: List[str]
username: Optional[str]
```

The `typing` module should still be used when it provides functionality that does not have an equivalent built-in syntax:

```python
from typing import Literal, Protocol, TypeVar, TypedDict
```

## Code Quality

### Backend

The backend uses:

* Ruff for linting and formatting.
* mypy for static type checking.
* pytest for testing.
* pre-commit for local automated checks.

Before creating a commit, code should pass:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest
```

### Frontend

The frontend uses:

* ESLint for linting.
* Prettier for formatting.
* TypeScript for static type checking.

Frontend code should follow the configured project rules and must pass the corresponding checks before being merged.

## Git Workflow

ParserHub uses the following long-lived branches:

```text
main
develop
```

### `main`

`main` contains production-ready code.

Direct commits to `main` should not be made.

Changes should be merged through a Pull Request.

### `develop`

`develop` contains the current development version of the project.

Feature and fix branches are normally created from `develop` and merged back into `develop`.

Changes should be reviewed through a Pull Request when practical.

## Branch Naming

Branches should follow one of the following formats:

```text
<type>/<issue-number>-<short-description>
<type>/<short-description>
````

When a branch is associated with a GitHub Issue, the issue number must be included.

Examples:

```text
feat/12-user-authentication
fix/27-login-validation
refactor/34-parser-registry
docs/41-development-guide
test/52-parser-service-tests
chore/18-update-dependencies
ci/23-improve-backend-checks
```

When a branch is not associated with a GitHub Issue, the issue number can be omitted:

```text
docs/update-readme
chore/update-uv
ci/update-workflow
```

Use lowercase words separated by hyphens.

The branch type should describe the purpose of the change.

### Branch Types

| Type       | Purpose                                      |
| ---------- | -------------------------------------------- |
| `feat`     | New functionality                            |
| `fix`      | Bug fix                                      |
| `refactor` | Code restructuring without changing behavior |
| `docs`     | Documentation changes                        |
| `test`     | Adding or modifying tests                    |
| `chore`    | Maintenance tasks                            |
| `ci`       | CI/CD configuration                          |
| `perf`     | Performance improvements                     |

## Commit Convention

ParserHub follows the **Conventional Commits** specification.

The basic format is:

```text
<type>(<scope>): <description>
```

Examples:

```text
feat(auth): add user registration
fix(auth): validate duplicate email
docs(development): document branch naming
refactor(parser): simplify parser registry
test(auth): add registration tests
chore(deps): update project dependencies
ci(github): run backend checks
```

### Commit Types

| Type       | Purpose                            |
| ---------- | ---------------------------------- |
| `feat`     | Introduces a new feature           |
| `fix`      | Fixes a bug                        |
| `docs`     | Documentation changes              |
| `refactor` | Code restructuring                 |
| `test`     | Adds or modifies tests             |
| `chore`    | Maintenance tasks                  |
| `ci`       | CI/CD changes                      |
| `perf`     | Performance improvements           |
| `build`    | Build system or dependency changes |

### Commit Header Rules

The commit header should:

* use lowercase for the type;
* use an optional scope when it adds useful context;
* use a short imperative description;
* not end with a period;
* describe what the commit does, not why it was done.

Good:

```text
feat(auth): add JWT authentication
```

Bad:

```text
Added JWT authentication.
```

Bad:

```text
feat: changes
```

Bad:

```text
feat: I added authentication because we need login
```

### Commit Scope

Use a scope when it makes the commit easier to understand.

Common scopes include:

```text
backend
frontend
auth
api
parser
database
github
docker
deps
docs
```

Examples:

```text
feat(backend): add health check endpoint
feat(auth): add password hashing
fix(api): handle invalid request body
docs(architecture): document service layer
ci(github): add backend test job
chore(deps): update FastAPI
```

## Issue References

When a commit is related to a GitHub Issue, the issue should be referenced when useful.

For example:

```text
feat(auth): add user registration (#12)
```

or in the commit body:

```text
feat(auth): add user registration

Refs #12
```

The branch name should also contain the issue number when possible:

```text
feat/12-user-registration
```

This keeps the relationship between the Issue, branch, Pull Request, and commits clear.

## Pull Requests

Pull Requests should:

1. Have a clear title following Conventional Commits.
2. Reference the related GitHub Issue.
3. Explain what was changed.
4. Explain any important implementation decisions.
5. Pass all required CI checks.
6. Avoid unrelated changes.

Example PR title:

```text
feat(auth): add user registration
```

Example:

```text
Closes #12
```

can be used in the PR description when the Pull Request completely resolves the Issue.

## General Rules

* Do not commit secrets or credentials.
* Do not commit `.env` files containing real credentials.
* Do not use `print()` for application logging.
* Use the project's logging system.
* Do not disable linting or type checking to hide errors.
* Do not ignore failing tests without a documented reason.
* Keep commits focused on one logical change.
* Avoid mixing unrelated changes in a single commit.
* Prefer small, understandable Pull Requests.
* Update documentation when a development or architectural rule changes.
