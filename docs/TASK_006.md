# TASK_006.md

---

# TASK 006

Version: 1.0

Status: Pending

Sprint: Sprint 2

Title

Scheduler & Automatic Data Synchronization

---

# Objective

Implement the Scheduler responsible for executing automatic synchronization between the NASA EONET API and the HELIX database.

The Scheduler orchestrates the complete synchronization pipeline by invoking existing services in the correct sequence.

No business logic should be implemented inside the Scheduler.

---

# Background

The HELIX architecture separates scheduling from business logic.

The Scheduler is responsible only for controlling execution timing and calling existing services.

Reference Documents

* HELIX_SPEC.md
* 01_SYSTEM_ARCHITECTURE.md
* 02_DATABASE_DESIGN.md
* RULES.md
* 05_CODING_RULES.md

---

# Scope

This task includes

* Create Scheduler Module.
* Configure APScheduler.
* Execute synchronization automatically.
* Execute synchronization immediately at application startup.
* Record synchronization logs.
* Refresh summary collections after successful synchronization.
* Continue execution after failures.

---

# Out of Scope

This task does NOT include

* Dashboard
* REST API
* HTML
* CSS
* JavaScript
* MapLibre
* Charts

---

# Input

Input comes from

```text
Scheduler Trigger

↓

NASA Fetch Service

↓

Transformer Service

↓

Repository

↓

Aggregation Service
```

---

# Output

Automatic synchronization cycle running continuously.

MongoDB is updated periodically without user interaction.

---

# Files to Create

```text
backend/scheduler/

scheduler.py
```

---

# Files to Modify

```text
app.py
```

Register and start the Scheduler during application startup.

---

# Scheduler Responsibilities

The Scheduler must execute the following sequence.

```text
Start Synchronization

↓

Fetch NASA Events

↓

Transform Events

↓

Upsert MongoDB Documents

↓

Generate Summary Collections

↓

Write Sync Log

↓

Finish
```

Every synchronization must complete this sequence in order.

---

# Scheduler Configuration

Scheduler Library

```text
APScheduler
```

Execution Interval

Read from

```text
.env
```

Variable

```text
FETCH_INTERVAL
```

The interval must never be hardcoded.

---

# Startup Behavior

When the application starts

1.

Initialize MongoDB Connection.

2.

Initialize Scheduler.

3.

Execute one synchronization immediately.

4.

Start periodic execution.

---

# Synchronization Logging

Create one synchronization log for every execution.

Store the following information.

```text
sync_id

started_at

finished_at

inserted

updated

failed

duration

status
```

Store the log inside

```text
sync_logs
```

---

# Failure Strategy

If synchronization fails

* Log the error.
* Record failure in sync_logs.
* Continue the next scheduled execution.
* Do not terminate Flask.
* Do not terminate APScheduler.

---

# Scheduler Rules

The Scheduler

* Must not contain MongoDB queries.
* Must not contain aggregation logic.
* Must not contain transformation logic.
* Must only orchestrate service execution.

---

# Logging

Log

* Scheduler Started
* Synchronization Started
* Fetch Completed
* Transformation Completed
* Database Updated
* Aggregation Completed
* Synchronization Finished
* Synchronization Failed

---

# Acceptance Criteria

Task is complete when

* Scheduler starts successfully.
* Synchronization executes automatically.
* Synchronization executes immediately at startup.
* Summary collections refresh successfully.
* Sync logs are generated.
* Application remains running after synchronization.

---

# Validation Checklist

Verify

* Scheduler starts successfully.
* Interval loaded from .env.
* Automatic synchronization works.
* Startup synchronization works.
* Sync log created.
* No syntax errors.
* No unused imports.

---

# Required Screenshots

Capture

1.

Scheduler Started

2.

Startup Synchronization

3.

Periodic Synchronization

4.

Sync Logs Collection

5.

MongoDB Updated

6.

Terminal Output

---

# Documentation Required

Prepare

* Scheduler Architecture Explanation
* Synchronization Workflow Explanation
* APScheduler Configuration Explanation
* Sync Log Explanation

---

# Deliverables

* scheduler.py
* Automatic Synchronization
* Startup Synchronization
* Sync Log Generation
* Working Scheduler

---

# Dependencies

TASK_005

---

# Next Task

TASK_007

REST API Implementation

---

# Completion Status

Pending

---

# Notes

The Scheduler acts only as an orchestrator.

All business logic must remain inside their respective services.

The Scheduler must not directly manipulate MongoDB documents except for invoking existing services.

---

End of Document
