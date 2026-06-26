# RULES.md

---

# HELIX Development Rules

Version: 1.0

Status: Approved

This document defines the mandatory development rules for the HELIX project.

Every implementation must follow these rules.

No rule may be ignored unless explicitly approved.

---

# 1. General Rules

* Do not change the project architecture.
* Do not create additional features outside the specification.
* Do not rename existing folders or files.
* Do not modify the project structure.
* Do not introduce new frameworks or libraries without approval.
* Keep every module small, modular, and maintainable.

---

# 2. Technology Rules

## Frontend

Allowed

* HTML5
* Bootstrap 5
* Vanilla JavaScript
* MapLibre GL JS
* Chart.js

Not Allowed

* React
* Vue
* Angular
* Tailwind CSS
* jQuery

---

## Backend

Allowed

* Python 3.12
* Flask
* APScheduler
* Requests
* PyMongo

Not Allowed

* FastAPI
* Django
* Express.js

---

## Database

Allowed

* MongoDB Community Edition

Development Database

localhost:27017

Database Name

helix

Not Allowed

* MySQL
* PostgreSQL
* SQLite
* Firebase

---

# 3. Folder Rules

All files must follow PROJECT_TREE.md.

No duplicate modules.

No duplicate folders.

No temporary source files.

No unused files.

---

# 4. API Rules

All REST APIs must use Flask Blueprint.

Every route must only perform:

* Request validation
* Service invocation
* Response generation

Business logic inside Route files is prohibited.

---

# 5. Service Rules

Every business process must be implemented inside Service Layer.

Examples:

* NASA Fetch
* Data Transformation
* MongoDB Query
* Aggregation
* Search
* Dashboard Summary

Services must not render HTML.

Services must not return templates.

Services return processed data only.

---

# 6. Database Rules

MongoDB connection must exist only inside

backend/database/

Indexes must be created automatically during initialization.

Raw API response must never be stored directly.

Every incoming document must pass through Transformer Service.

Database queries must be implemented only inside Service Layer.

---

# 7. Configuration Rules

All configuration values must come from

.env

Examples

* Mongo URI
* Database Name
* Scheduler Interval
* API Base URL

Hardcoded configuration values are prohibited.

---

# 8. Code Style Rules

* Use snake_case for variables and functions.
* Use PascalCase for classes.
* Use UPPER_CASE for constants.
* Use type hints whenever possible.
* Every public function must include a docstring.
* Keep functions focused on a single responsibility.

---

# 9. Frontend Rules

Desktop First.

Single Page Dashboard.

Use Bootstrap Grid.

Glassmorphism UI.

Dark Grey Theme.

Map visualization must use MapLibre.

Charts must use Chart.js.

No page reload during interaction.

Use Fetch API for backend communication.

---

# 10. Dashboard Rules

Dashboard consists of:

* Navigation Bar
* Summary Cards
* Interactive Map
* Event Detail Panel
* Category Filter
* Time Slider
* Analytics Charts
* Live Event Feed

No additional pages unless specified.

---

# 11. Scheduler Rules

Scheduler must run automatically.

Scheduler responsibilities:

* Fetch NASA EONET API
* Transform data
* Insert or update MongoDB
* Refresh Summary Collections
* Write Sync Logs

Scheduler must never directly communicate with frontend.

---

# 12. MongoDB Rules

Use Query-Oriented Design.

Implement:

* Embedded Documents
* Reference Documents
* Denormalization
* Indexing
* Aggregation Pipeline

Collections will follow

02_DATABASE_DESIGN.md

---

# 13. Error Handling Rules

Every exception must be handled.

Do not expose internal errors to frontend.

Log all unexpected errors.

Return consistent JSON responses.

---

# 14. Logging Rules

Application logs must include:

* Startup
* Scheduler Execution
* API Request
* Database Connection
* Synchronization Result
* Error

Console output should remain readable.

---

# 15. Git Rules

Recommended Commit Format

feat:

fix:

refactor:

docs:

test:

chore:

One feature per commit.

---

# 16. Documentation Rules

Every completed task must include:

* Updated source code
* Screenshot
* Screenshot description
* Testing result

No task is considered complete without documentation.

---

# 17. Development Workflow

Every task follows the same sequence.

Read Task

↓

Implement

↓

Test

↓

Review

↓

Screenshot

↓

Documentation

↓

Complete

---

# 18. Final Rule

Gemini CLI is responsible only for implementation.

Architecture decisions, database design, API design, documentation structure, and project organization are defined by the official engineering documents and must not be changed during implementation.

---

End of Document.
