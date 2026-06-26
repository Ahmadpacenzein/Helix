# 05_CODING_RULES.md

---

# HELIX Coding Standards

Version: 1.0

Status: Approved

Reference

* HELIX_SPEC.md
* PROJECT_TREE.md
* RULES.md

---

# 1. Purpose

This document defines the coding standards for the HELIX project.

Every source file created during development must follow these standards.

These rules ensure consistency, readability, maintainability, and modularity.

---

# 2. General Principles

The project follows these principles.

* Keep code simple.
* Keep code modular.
* Keep code readable.
* Keep functions focused on one responsibility.
* Avoid unnecessary complexity.
* Avoid duplicate implementations.

---

# 3. Python Standards

Python Version

```text
Python 3.12
```

Required

* Type Hint
* Docstring
* Modular Functions

Avoid

* Global variables
* Hardcoded values
* Duplicate logic

---

# 4. Naming Convention

## Variables

snake_case

Example

```python
event_count

last_sync

country_name
```

---

## Functions

snake_case

Example

```python
fetch_events()

create_indexes()

generate_dashboard_summary()
```

---

## Classes

PascalCase

Example

```python
MongoConnection

EventService

DashboardService
```

---

## Constants

UPPER_CASE

Example

```python
DATABASE_NAME

FETCH_INTERVAL
```

---

# 5. File Responsibilities

Each file has one responsibility only.

Example

```text
dashboard_service.py

↓

Dashboard Business Logic
```

Not

```text
Dashboard

+

Search

+

Mongo Connection
```

Mixing responsibilities is prohibited.

---

# 6. Function Rules

Each function should

* Perform one task only.
* Return predictable output.
* Handle expected errors.
* Include a docstring.
* Include type hints.

Avoid functions with excessive length.

---

# 7. API Route Rules

Route files must only:

* Receive Request
* Validate Parameters
* Call Service
* Return JSON

Routes must never:

* Query MongoDB
* Perform Aggregation
* Execute Business Logic

---

# 8. Service Layer Rules

Services are responsible for

* Business Logic
* Database Operations
* Aggregation
* Data Transformation

Services must never

* Render HTML
* Return Templates

---

# 9. Database Rules

Database access is restricted to the Service Layer.

All database configuration must use

```text
config.py
```

Connection logic must remain inside

```text
backend/database/
```

---

# 10. Configuration Rules

Never hardcode values.

Always use environment variables.

Examples

* MongoDB URI
* Database Name
* Scheduler Interval
* API URL

---

# 11. JavaScript Standards

Use

* ES6 Syntax
* Fetch API
* Async / Await

Avoid

* jQuery
* Inline JavaScript
* Global Variables

---

# 12. CSS Standards

Organize styles by responsibility.

Files

```text
style.css

↓

Global Styles

dashboard.css

↓

Dashboard Layout

components.css

↓

Reusable Components
```

Inline CSS is prohibited.

---

# 13. HTML Standards

Use semantic HTML.

Examples

* header
* nav
* section
* article
* footer

Avoid unnecessary nesting.

---

# 14. Logging Standards

Application logs should include

* Application Startup
* MongoDB Connection
* Scheduler Execution
* API Request
* Synchronization Result
* Error Message

Logs should remain concise and readable.

---

# 15. Error Handling

Every exception should be handled.

Unexpected exceptions should

* Be logged.
* Return a consistent error response.
* Keep the application running.

Application crashes caused by unhandled exceptions are not acceptable.

---

# 16. Code Duplication

Duplicate code is prohibited.

If functionality is reused, create a reusable helper or service.

---

# 17. Comments

Write comments only when they improve understanding.

Avoid comments that describe obvious code.

Docstrings remain mandatory for public functions.

---

# 18. Import Rules

Organize imports in the following order.

1. Python Standard Library

2. Third-party Libraries

3. Local Project Modules

Unused imports must be removed.

---

# 19. Testing Requirements

Before completing any task

Verify

* No syntax errors
* Application starts successfully
* API works correctly
* MongoDB connection succeeds
* No duplicate code
* No unused imports

---

# 20. Code Review Checklist

Before marking a task as complete

Confirm

* Follows PROJECT_TREE.md
* Follows HELIX_SPEC.md
* Follows RULES.md
* Uses modular architecture
* Uses service layer
* Uses environment variables
* Uses consistent naming
* Contains no hardcoded values

---

# 21. Completion Standard

A development task is considered complete only when

* Source code is implemented.
* Code follows all coding standards.
* Testing is successful.
* Required screenshots are captured.
* Documentation is prepared.

Implementation without documentation is considered incomplete.

---

End of Document
