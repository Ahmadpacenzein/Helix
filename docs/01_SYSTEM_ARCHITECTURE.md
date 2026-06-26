# 01_SYSTEM_ARCHITECTURE.md

---

# HELIX System Architecture

Version: 1.0

Status: Approved

Reference:

* HELIX_SPEC.md
* PROJECT_TREE.md
* RULES.md

---

# 1. Overview

HELIX is designed using a modular layered architecture.

Each layer has a single responsibility and communicates only with its adjacent layer.

This architecture improves maintainability, scalability, testing, and separation of concerns.

---

# 2. High-Level Architecture

```text
                     NASA EONET API
                            │
                            ▼
                    Fetch Service
                            │
                            ▼
                  Transformer Service
                            │
                            ▼
                     MongoDB Database
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     Events       Summary Collections    Sync Logs
                            │
                            ▼
                     Service Layer
                            │
                            ▼
                      Flask REST API
                            │
                            ▼
                   HELIX Web Dashboard
```

---

# 3. Architecture Layers

## External Layer

Responsible for retrieving disaster data from NASA EONET API.

Responsibilities:

* Request data
* Receive JSON response
* Pass data to Transformer

No database interaction is allowed.

---

## Transformation Layer

Responsible for converting NASA response into HELIX schema.

Responsibilities:

* Data mapping
* Data validation
* Data normalization
* Field generation

No dashboard interaction is allowed.

---

## Database Layer

Responsible for MongoDB operations.

Responsibilities:

* Connection
* Insert
* Update
* Index
* Aggregation

No UI logic is allowed.

---

## Service Layer

Responsible for business logic.

Responsibilities:

* Dashboard summary
* Event processing
* Analytics
* Search
* Synchronization

No HTML rendering is allowed.

---

## API Layer

Responsible for exposing REST endpoints.

Responsibilities:

* Receive request
* Validate request
* Call service
* Return JSON response

No MongoDB query is allowed.

---

## Presentation Layer

Responsible for data visualization.

Responsibilities:

* Dashboard
* Charts
* Interactive Map
* Filters
* Search
* Time Slider

No business logic is allowed.

---

# 4. Data Flow

The official system workflow is:

```text
Scheduler
      │
      ▼
Fetch NASA API
      │
      ▼
Receive JSON
      │
      ▼
Transform Data
      │
      ▼
Insert / Update MongoDB
      │
      ▼
Generate Summary Collections
      │
      ▼
Expose REST API
      │
      ▼
Dashboard Refresh
```

Every synchronization follows this exact workflow.

---

# 5. Synchronization Flow

Each scheduler execution performs the following sequence.

1. Request latest disaster events.

2. Validate response.

3. Transform NASA schema into HELIX schema.

4. Perform Upsert using Event ID.

5. Refresh aggregation collections.

6. Store synchronization log.

7. Wait until next execution cycle.

---

# 6. Data Ownership

Each module owns its own responsibility.

## Fetch Service

Owns communication with NASA API.

---

## Transformer

Owns schema conversion.

---

## Database

Owns data persistence.

---

## Aggregation

Owns summary collections.

---

## API

Owns REST communication.

---

## Frontend

Owns visualization only.

---

# 7. Communication Rules

Allowed communication:

NASA API

↓

Fetcher

↓

Transformer

↓

Database

↓

Service

↓

API

↓

Frontend

Reverse communication is prohibited.

Frontend must never access MongoDB directly.

---

# 8. Error Handling Flow

If an error occurs during synchronization:

Scheduler

↓

Log Error

↓

Skip Current Cycle

↓

Continue Next Cycle

Application must continue running.

Scheduler must never terminate because of one failed synchronization.

---

# 9. Scheduler Architecture

Scheduler runs independently from the dashboard.

Responsibilities:

* Fetch data
* Transform data
* Update database
* Refresh summaries
* Create synchronization logs

Dashboard never triggers synchronization.

---

# 10. Summary Collection Strategy

Dashboard statistics must always read from Summary Collections.

The Events collection is reserved for:

* Event Detail
* Search Result
* Timeline
* Time Slider

Statistics must never be calculated directly from Events during page rendering.

---

# 11. Scalability Consideration

The architecture is designed to allow future replacement of the data source without changing the dashboard.

If NASA EONET is replaced by another disaster provider, only the Fetch Service and Transformer require modification.

All remaining modules remain unchanged.

---

# 12. Architecture Principles

The architecture follows the following principles.

* Single Responsibility Principle
* Layer Separation
* Modular Design
* Query-Oriented Database Design
* Service-Based Business Logic
* Read-Optimized Dashboard

These principles must remain unchanged throughout the project.

---

End of Document
