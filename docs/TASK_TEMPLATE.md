# TASK_TEMPLATE.md

---

# TASK_XXX

Version: 1.0

Status: Pending

Sprint: Sprint X

---

# Objective

Describe the primary objective of this task.

The objective must be concise, measurable, and implementation-focused.

---

# Background

Explain why this task exists.

Reference the related engineering document if applicable.

Example:

* HELIX_SPEC.md
* 01_SYSTEM_ARCHITECTURE.md
* 02_DATABASE_DESIGN.md
* 03_API_SPECIFICATION.md
* 04_FRONTEND_SPEC.md

---

# Scope

List everything included in this task.

Example:

* Create configuration file
* Create Flask Blueprint
* Create MongoDB connection

Only items listed here may be implemented.

---

# Out of Scope

List everything explicitly excluded.

No implementation outside this section is allowed.

---

# Input

Describe the expected inputs.

Examples:

* Existing project structure
* Environment variables
* NASA API endpoint
* MongoDB database

---

# Output

Describe the expected output after task completion.

Example:

* Running Flask application
* Connected MongoDB database
* Working REST endpoint

---

# Files to Create

List every new file.

Example:

backend/database/mongo.py

backend/database/indexes.py

---

# Files to Modify

List existing files that must be modified.

If none, write:

None

---

# Implementation Requirements

Describe the implementation requirements.

Examples:

* Follow RULES.md
* Follow PROJECT_TREE.md
* Follow HELIX_SPEC.md
* Use modular architecture
* Keep functions small
* Include type hints
* Include docstrings

---

# Acceptance Criteria

The task is considered complete only if all conditions below are satisfied.

Example:

* Flask starts successfully.
* MongoDB connects successfully.
* No runtime errors.
* Source code follows coding standards.

---

# Validation Checklist

* Project builds successfully.
* No syntax errors.
* No unused imports.
* No duplicate functions.
* No duplicate files.
* No hardcoded configuration.
* Code formatted consistently.

Every item must be completed.

---

# Expected Deliverables

The implementation must produce:

* Source code
* Updated project files
* Working functionality

---

# Required Screenshots

Capture the following screenshots after implementation.

Example:

* Terminal output
* Browser result
* MongoDB Compass
* Project folder

Do not capture unnecessary screenshots.

---

# Documentation Required

Prepare the following documentation after implementation.

* Screenshot explanation
* Technical explanation
* Testing result

Documentation is mandatory.

---

# Dependencies

List tasks that must already be completed.

Example:

TASK_001

If none, write:

None

---

# Next Task

Specify the next task after successful completion.

Example:

TASK_002

---

# Completion Status

Status

Pending

In Progress

Completed

Select one status only.

---

# Notes

Use this section only for implementation notes directly related to this task.

Do not introduce new features or architecture changes.

---

End of Template
