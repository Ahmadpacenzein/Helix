# TASK_004.md

---

# TASK 004

Version: 1.0

Status: Pending

Sprint: Sprint 1

Title

MongoDB Repository & Data Persistence

---

# Objective

Implement the MongoDB Repository responsible for storing transformed HELIX documents into MongoDB.

This task establishes the persistence layer of the application using an Upsert strategy to prevent duplicate disaster events.

---

# Background

After the Fetch Service retrieves data and the Transformer converts it into the HELIX schema, the application requires a persistence layer to store the documents inside MongoDB.

The Repository is responsible only for database operations and must not contain business logic.

Reference Documents

* HELIX_SPEC.md
* 02_DATABASE_DESIGN.md
* 05_CODING_RULES.md
* RULES.md

---

# Scope

This task includes

* Create MongoDB Repository.
* Connect Repository with MongoDB.
* Implement Event Upsert.
* Create database collections automatically.
* Create required indexes automatically.
* Store transformed documents.
* Update existing documents.
* Handle database exceptions.

---

# Out of Scope

This task does NOT include

* NASA Fetching
* Data Transformation
* Scheduler
* Aggregation
* Dashboard
* REST API

---

# Input

Input comes only from

Transformer Service

Example

```text
NASA JSON

↓

Transformer

↓

HELIX Event Document

↓

Repository
```

---

# Output

The transformed HELIX event document is stored inside MongoDB.

Documents are inserted or updated based on the Event ID.

---

# Files to Create

```text
backend/services/

sync_service.py

backend/database/

indexes.py
```

---

# Files to Modify

```text
backend/database/

mongo.py
```

---

# Repository Responsibilities

The Repository must

* Connect to MongoDB.
* Access Events collection.
* Perform Upsert.
* Return operation status.
* Handle duplicate prevention.

---

# Collection Responsibilities

Repository writes only to

```text
events
```

No Summary Collections are generated in this task.

---

# Upsert Strategy

Use

```text
event_id
```

as the unique identifier.

Behavior

If Event ID does not exist

↓

Insert New Document

If Event ID already exists

↓

Update Existing Document

Duplicate documents are prohibited.

---

# Index Creation

Automatically create the following indexes.

| Collection | Field                | Type       |
| ---------- | -------------------- | ---------- |
| events     | event_id             | Unique     |
| events     | category.name        | Ascending  |
| events     | country              | Ascending  |
| events     | status               | Ascending  |
| events     | latest_geometry.date | Descending |

Indexes must be created only once.

---

# Repository Functions

The Repository should expose reusable functions.

Example

```python
upsert_event()

create_indexes()

get_collection()
```

Implementation details are left to the developer as long as the architecture remains unchanged.

---

# Error Handling

Handle

* MongoDB Connection Failure
* Duplicate Key Error
* Invalid Document
* Write Failure

Application must continue running whenever possible.

Errors must be logged.

---

# Logging

Log

* Database Connected
* Collection Ready
* Index Created
* Document Inserted
* Document Updated
* Database Error

---

# Acceptance Criteria

Task is complete when

* MongoDB connection succeeds.
* Events collection is created automatically.
* Required indexes exist.
* Upsert works correctly.
* Duplicate Event IDs are prevented.
* Repository contains no business logic.
* No scheduler code exists.

---

# Validation Checklist

Verify

* Collection created successfully.
* Indexes created successfully.
* Insert works.
* Update works.
* Duplicate prevention works.
* No syntax errors.
* No unused imports.

---

# Required Screenshots

Capture

1.

MongoDB Compass

Database Created

2.

Events Collection

3.

Indexes

4.

Inserted Document

5.

Updated Document

6.

Terminal Output

---

# Documentation Required

Prepare

* MongoDB Repository Explanation
* Upsert Strategy Explanation
* Index Creation Explanation
* Database Persistence Explanation

---

# Deliverables

* MongoDB Repository
* Automatic Collection Creation
* Automatic Index Creation
* Upsert Implementation
* Working Database Persistence

---

# Dependencies

TASK_003

---

# Next Task

TASK_005

Aggregation Service & Summary Collections

---

# Completion Status

Pending

---

# Notes

This task is limited to MongoDB persistence.

Do not implement aggregation.

Do not implement scheduler.

Do not implement REST API.

Do not implement dashboard functionality.

---

End of Document
