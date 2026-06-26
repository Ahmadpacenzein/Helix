# PROJECT_TREE.md

---

# HELIX Project Structure

This document defines the official directory and file structure of the HELIX project.

No additional files or folders should be created unless approved by the Tech Lead.

This structure must remain consistent throughout the project.

---

# Root Directory

```text
HELIX/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── backend/
├── frontend/
├── docs/
├── screenshots/
├── tests/
└── scripts/
```

---

# Backend

```text
backend/
│
├── api/
│   ├── dashboard.py
│   ├── events.py
│   ├── analytics.py
│   └── search.py
│
├── database/
│   ├── mongo.py
│   └── indexes.py
│
├── scheduler/
│   └── scheduler.py
│
├── services/
│   ├── nasa_fetcher.py
│   ├── transformer.py
│   ├── aggregation.py
│   ├── sync_service.py
│   ├── dashboard_service.py
│   ├── event_service.py
│   ├── analytics_service.py
│   └── search_service.py
│
├── models/
│   ├── event.py
│   ├── dashboard_summary.py
│   ├── category_summary.py
│   ├── country_summary.py
│   └── sync_log.py
│
└── utils/
    ├── logger.py
    ├── helpers.py
    └── response.py
```

---

# Frontend

```text
frontend/
│
├── templates/
│   └── index.html
│
└── static/
    │
    ├── css/
    │   ├── style.css
    │   ├── dashboard.css
    │   └── components.css
    │
    ├── js/
    │   ├── app.js
    │   ├── map.js
    │   ├── dashboard.js
    │   ├── charts.js
    │   ├── search.js
    │   ├── timeline.js
    │   └── api.js
    │
    └── img/
```

---

# Documentation

```text
docs/
│
├── 00_PROJECT_OVERVIEW.md
├── HELIX_SPEC.md
├── PROJECT_TREE.md
├── RULES.md
├── TASK_TEMPLATE.md
│
├── 01_SYSTEM_ARCHITECTURE.md
├── 02_DATABASE_DESIGN.md
├── 03_API_SPECIFICATION.md
├── 04_FRONTEND_SPEC.md
├── 05_CODING_RULES.md
│
├── TASK_001.md
├── TASK_002.md
├── TASK_003.md
├── TASK_004.md
├── TASK_005.md
├── TASK_006.md
├── TASK_007.md
├── TASK_008.md
├── TASK_009.md
└── TASK_010.md
```

---

# Screenshots

```text
screenshots/
│
├── 01_environment/
├── 02_database/
├── 03_fetcher/
├── 04_scheduler/
├── 05_dashboard/
├── 06_map/
├── 07_analytics/
├── 08_testing/
└── 09_final/
```

---

# Tests

```text
tests/
│
├── test_database.py
├── test_fetcher.py
├── test_transformer.py
├── test_api.py
└── test_dashboard.py
```

---

# Scripts

```text
scripts/
│
├── init_database.py
├── create_indexes.py
└── reset_database.py
```

---

# File Responsibilities

## app.py

Application entry point.

---

## config.py

Application configuration loader.

---

## backend/api

Contains all REST API endpoints.

No business logic is allowed.

---

## backend/services

Contains all business logic.

Responsible for data processing and communication with MongoDB.

---

## backend/database

Contains MongoDB connection and index creation.

---

## backend/models

Contains MongoDB document models.

---

## backend/scheduler

Responsible for periodic synchronization with NASA EONET API.

---

## backend/utils

Contains reusable helper functions.

---

## frontend

Contains all user interface components.

---

## docs

Contains all engineering documents and development tasks.

---

## screenshots

Contains screenshots for documentation and final report.

---

## tests

Contains application testing scripts.

---

## scripts

Contains utility scripts for initializing and maintaining the database.

---

# Project Structure Rules

* Every file must follow this structure.
* No duplicate modules are allowed.
* No duplicate services are allowed.
* No business logic inside API routes.
* No MongoDB query inside frontend.
* No file creation outside this structure without project approval.

---

End of Document.
