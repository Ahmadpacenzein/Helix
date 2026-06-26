# HELIX_SPEC.md

---

# HELIX Technical Specification

Version: 1.0

Status: Approved

Project Name: HELIX

This document serves as the master technical specification for the HELIX project. Every engineering document, development task, implementation, and code review must follow the specifications defined in this document.

This specification is considered the single source of truth throughout the entire project lifecycle.

---

# 1. Project Goal

HELIX is a desktop-first web application designed to monitor global natural disasters using real-time data provided by the NASA EONET API.

The project focuses on implementing NoSQL Data Modeling Architecture using MongoDB, demonstrating query-oriented schema design, embedded documents, reference documents, denormalization, indexing, aggregation, and query optimization.

---

# 2. System Architecture

```
NASA EONET API
        │
        ▼
Fetch Service
        │
        ▼
Data Transformer
        │
        ▼
MongoDB
        │
 ┌──────┼────────────────────┐
 ▼      ▼                    ▼
Events  Summary Collections  Sync Logs
        │
        ▼
REST API (Flask)
        │
        ▼
HELIX Dashboard
```

Every incoming dataset must pass through the Transformer before being stored inside MongoDB.

No component is allowed to bypass this architecture.

---

# 3. Technology Stack

## Frontend

* HTML5
* Bootstrap 5
* Vanilla JavaScript
* MapLibre GL JS
* Chart.js

## Backend

* Python 3.12
* Flask
* APScheduler

## Database

* MongoDB Community Edition
* MongoDB Compass

## External Service

* NASA EONET API

---

# 4. Development Principles

The following principles are mandatory.

### Principle 1

Dashboard must never communicate directly with MongoDB.

All communication must pass through Flask REST API.

---

### Principle 2

All NASA responses must pass through the Transformer layer before database insertion.

Raw responses must never be stored directly.

---

### Principle 3

MongoDB schema must follow query-oriented design.

Schema is designed based on dashboard requirements instead of API structure.

---

### Principle 4

Dashboard statistics must read from Summary Collections instead of the Events collection.

---

### Principle 5

Configuration values must never be hardcoded.

Every configurable value must be stored inside `.env`.

---

### Principle 6

Every MongoDB query must be implemented inside the Service Layer.

Route files must never contain database logic.

---

# 5. Project Scope

The following modules are included.

* NASA Fetcher
* Data Transformer
* MongoDB Integration
* Aggregation Service
* Scheduler
* REST API
* Dashboard
* Interactive Map
* Search
* Filter
* Time Slider

The following modules are excluded.

* Login
* Authentication
* Authorization
* Machine Learning
* Artificial Intelligence
* Mobile Application
* Notification System

---

# 6. Database Design Strategy

MongoDB will use a query-oriented schema.

The project must demonstrate:

* Embedded Document
* Reference Document
* Denormalization
* Indexing
* Aggregation Pipeline

Collection design will be defined in `02_DATABASE_DESIGN.md`.

---

# 7. Dashboard Design Strategy

The dashboard will follow a Single Page Application layout.

Main sections include:

* Navigation Bar
* Summary Cards
* Interactive Map
* Live Event Feed
* Category Filter
* Time Slider
* Analytics Charts
* Event Detail Panel

Dashboard specification will be defined in `04_FRONTEND_SPEC.md`.

---

# 8. Backend Design Strategy

Backend responsibilities include:

* Fetch NASA API
* Transform incoming data
* Store documents
* Generate summary collections
* Expose REST APIs
* Execute scheduled synchronization

REST API specification will be defined in `03_API_SPECIFICATION.md`.

---

# 9. Documentation Strategy

Every completed task must produce:

* Source Code
* Screenshot
* Screenshot Description
* Testing Result
* Report Material

No implementation task is considered complete without documentation.

---

# 10. Development Workflow

The official development workflow is:

Planning

↓

Architecture

↓

Database Design

↓

API Design

↓

Frontend Design

↓

Gemini CLI Implementation

↓

Code Review

↓

Testing

↓

Documentation

↓

Final Report

No development stage may skip a previous stage.

---

# 11. Development Rules

The architecture defined in this specification is final.

No technology stack changes are allowed.

No feature additions are allowed unless explicitly requested by the Project Manager.

All future documents must follow this specification.

---

End of Specification
