# TASK_003.md

---

# TASK 003

Version: 1.0

Status: Pending

Sprint: Sprint 1

Title

NASA Data Transformation Service

---

# Objective

Implement the Transformer Service responsible for converting the raw NASA EONET response into the official HELIX MongoDB schema.

The Transformer is the only module allowed to convert external data into internal application data.

---

# Background

NASA EONET returns data optimized for API communication.

HELIX uses a Query-Oriented MongoDB schema designed for dashboard visualization and efficient aggregation.

This task creates the transformation layer between those two schemas.

Reference Documents

* HELIX_SPEC.md
* 01_SYSTEM_ARCHITECTURE.md
* 02_DATABASE_DESIGN.md
* RULES.md

---

# Scope

This task includes

* Create Transformer Service.
* Convert NASA JSON into HELIX schema.
* Validate required fields.
* Handle missing values.
* Normalize document structure.
* Extract latest geometry.
* Generate geometry history.
* Generate timestamps.
* Prepare document for MongoDB insertion.

---

# Out of Scope

This task does NOT include

* MongoDB
* Database Insert
* Aggregation
* Scheduler
* Dashboard
* REST API
* Country Reverse Geocoding

---

# Input

Input comes only from

NASA Fetch Service

Example

```text id="xtiq3i"
Raw NASA JSON

↓

Transformer
```

---

# Output

One HELIX Event Document.

Example

```text id="ewh5ko"
HELIX Event Schema
```

The output must follow exactly the schema defined in

02_DATABASE_DESIGN.md

---

# Files to Create

```text id="h6nrn0"
backend/services/

transformer.py
```

---

# Files to Modify

None

---

# Transformation Responsibilities

The transformer must

* Extract Event ID.
* Extract Title.
* Extract Description.
* Extract Category.
* Extract Status.
* Extract Sources.
* Extract Geometry History.
* Determine Latest Geometry.
* Generate created_at.
* Generate updated_at.

---

# Required Mapping

The transformed document must contain

```text id="crhcdj"
event_id

title

description

category

status

country

latest_geometry

geometry_history

sources

created_at

updated_at

sync_id
```

The document structure must exactly match

02_DATABASE_DESIGN.md

---

# Latest Geometry

The transformer must determine

```text id="93q6zz"
latest_geometry
```

using the latest geometry entry provided by NASA.

No additional processing is required.

---

# Geometry History

The transformer must preserve

```text id="2t8ezt"
geometry_history
```

from NASA.

The history is required for future Time Slider functionality.

---

# Missing Values

If optional fields are unavailable

Use

```text id="w35h6b"
null
```

or

```text id="c8gdz5"
[]
```

depending on the data type.

Transformation must never fail because of missing optional data.

---

# Validation

Reject documents when

* Event ID is missing.
* Title is missing.
* Category is missing.

Invalid documents must not continue to the next layer.

---

# Error Handling

Handle

* Missing fields
* Invalid geometry
* Invalid category
* Invalid response structure

Errors must be logged.

---

# Logging

Log

* Document Transformation Started
* Event ID
* Successful Transformation
* Invalid Document
* Transformation Failed

---

# Acceptance Criteria

Task is complete when

* Raw NASA JSON is converted successfully.
* Output follows HELIX schema.
* Missing values are handled.
* Invalid documents are rejected.
* No MongoDB code exists.
* No Aggregation code exists.

---

# Validation Checklist

Verify

* Output matches database schema.
* Geometry History preserved.
* Latest Geometry generated.
* Required fields validated.
* No syntax errors.
* No unused imports.

---

# Required Screenshots

Capture

1.

Raw NASA JSON

↓

2.

Transformed HELIX Document

↓

3.

Terminal Output

↓

4.

Project Structure

---

# Documentation Required

Prepare

* Data Transformation Explanation
* Schema Mapping Explanation
* Validation Explanation

---

# Deliverables

* transformer.py
* Valid HELIX Event Document
* Schema Mapping
* Validation Logic

---

# Dependencies

TASK_002

---

# Next Task

TASK_004

MongoDB Repository & Data Persistence

---

# Completion Status

Pending

---

# Notes

This task performs transformation only.

No database operations are allowed.

No scheduler operations are allowed.

No aggregation is allowed.

No dashboard logic is allowed.

---

End of Document
