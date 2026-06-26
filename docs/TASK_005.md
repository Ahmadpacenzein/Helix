# TASK_005.md

---

# TASK 005

Version: 1.0

Status: Pending

Sprint: Sprint 2

Title

Aggregation Service & Summary Collections

---

# Objective

Implement the Aggregation Service responsible for generating summary collections from the Events collection.

The generated summary collections will be used directly by the dashboard to improve query performance and reduce computation during page rendering.

---

# Background

HELIX applies a denormalization strategy by storing frequently accessed statistics in dedicated summary collections.

Instead of calculating statistics every dashboard request, aggregation results are generated after every successful synchronization.

Reference Documents

* HELIX_SPEC.md
* 02_DATABASE_DESIGN.md
* 05_CODING_RULES.md
* RULES.md

---

# Scope

This task includes

* Create Aggregation Service.
* Generate Dashboard Summary.
* Generate Country Summary.
* Generate Category Summary.
* Store aggregation results.
* Replace previous summary data.
* Handle aggregation errors.

---

# Out of Scope

This task does NOT include

* NASA Fetch
* Data Transformation
* Scheduler
* REST API
* Dashboard
* Search
* Timeline

---

# Input

Input comes only from

```text id="f5at5p"
events collection
```

---

# Output

Three summary collections.

```text id="ek8g4s"
dashboard_summary

country_summary

category_summary
```

---

# Files to Create

```text id="yblvcb"
backend/services/

aggregation.py
```

---

# Files to Modify

None

---

# Aggregation Responsibilities

The Aggregation Service must

* Read Events collection.
* Execute aggregation pipelines.
* Generate summary documents.
* Replace previous summary data.
* Store new summaries.

---

# Dashboard Summary

Collection

```text id="woy8xv"
dashboard_summary
```

Document

```text id="uqr0z4"
total_events

active_events

total_categories

total_countries

updated_today

last_sync

generated_at
```

Only one document exists inside this collection.

---

# Country Summary

Collection

```text id="jlwmkk"
country_summary
```

Generate one document per country.

Each document contains

```text id="95c0s8"
country

total_events

categories

updated_at
```

---

# Category Summary

Collection

```text id="5g9e4v"
category_summary
```

Generate one document per category.

Each document contains

```text id="cfh2dq"
category

total_events

updated_at
```

---

# Aggregation Strategy

Every execution follows

```text id="t4oq6d"
Read Events

↓

Aggregate

↓

Delete Previous Summary

↓

Insert New Summary

↓

Complete
```

Summary collections must always represent the latest database state.

---

# Aggregation Frequency

Aggregation is executed only after a successful synchronization cycle.

It is never executed from the frontend.

---

# Repository Rules

Aggregation must access only

```text id="u1vrvg"
events
```

Aggregation must write only to

```text id="sl9cjj"
dashboard_summary

country_summary

category_summary
```

---

# Error Handling

Handle

* Empty Events Collection
* Aggregation Failure
* MongoDB Write Failure

Errors must be logged.

Application must continue running.

---

# Logging

Log

* Aggregation Started
* Dashboard Summary Generated
* Country Summary Generated
* Category Summary Generated
* Aggregation Completed
* Aggregation Failed

---

# Acceptance Criteria

Task is complete when

* Dashboard Summary generated successfully.
* Country Summary generated successfully.
* Category Summary generated successfully.
* Previous summaries replaced correctly.
* No duplicate summary documents.
* Aggregation code remains modular.

---

# Validation Checklist

Verify

* dashboard_summary exists.
* country_summary exists.
* category_summary exists.
* Aggregation executes successfully.
* No syntax errors.
* No duplicate documents.
* No unused imports.

---

# Required Screenshots

Capture

1.

Dashboard Summary Collection

2.

Country Summary Collection

3.

Category Summary Collection

4.

Aggregation Result

5.

MongoDB Compass

6.

Terminal Output

---

# Documentation Required

Prepare

* Aggregation Service Explanation
* Denormalization Explanation
* Summary Collection Explanation
* MongoDB Aggregation Pipeline Explanation

---

# Deliverables

* aggregation.py
* dashboard_summary collection
* country_summary collection
* category_summary collection
* Working aggregation pipeline

---

# Dependencies

TASK_004

---

# Next Task

TASK_006

Scheduler & Automatic Data Synchronization

---

# Completion Status

Pending

---

# Notes

This task is responsible only for generating summary collections.

Do not implement scheduler.

Do not implement REST API.

Do not implement dashboard.

Do not implement frontend components.

---

End of Document
