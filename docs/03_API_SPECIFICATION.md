# 03_API_SPECIFICATION.md

---

# HELIX REST API Specification

Version: 1.0

Status: Approved

Reference

* HELIX_SPEC.md
* 01_SYSTEM_ARCHITECTURE.md
* 02_DATABASE_DESIGN.md

---

# 1. Overview

HELIX exposes REST APIs to provide disaster information for the frontend dashboard.

All frontend components must retrieve data exclusively through these APIs.

Direct database access from the frontend is prohibited.

All responses use JSON format.

---

# 2. Base URL

```text
http://localhost:5000/api
```

---

# 3. Standard Response Format

## Success Response

```json
{
    "success": true,
    "data": {}
}
```

---

## Error Response

```json
{
    "success": false,
    "message": "Error description"
}
```

---

# 4. Dashboard API

## GET /dashboard

Purpose

Return dashboard summary information.

Response

```json
{
    "success": true,
    "data": {

        "total_events": 0,

        "active_events": 0,

        "total_categories": 0,

        "total_countries": 0,

        "updated_today": 0,

        "last_sync": ""
    }
}
```

Used By

* Summary Cards

---

# 5. Events API

## GET /events

Purpose

Return disaster events for map visualization.

Query Parameters

| Parameter | Description          |
| --------- | -------------------- |
| country   | Filter by country    |
| category  | Filter by category   |
| status    | Filter by status     |
| date      | Filter by event date |

Response

```json
{
    "success": true,

    "data":[

    ]
}
```

Used By

* Interactive Map
* Time Slider
* Search Result

---

# 6. Event Detail API

## GET /events/{event_id}

Purpose

Return one disaster event.

Response

```json
{
    "success": true,

    "data":{

    }
}
```

Used By

* Event Detail Panel

---

# 7. Country Analytics API

## GET /analytics/country

Purpose

Return aggregated statistics grouped by country.

Response

```json
{
    "success": true,

    "data":[

    ]
}
```

Used By

* Top Countries Chart
* Choropleth Map

---

# 8. Category Analytics API

## GET /analytics/category

Purpose

Return aggregated statistics grouped by category.

Response

```json
{
    "success": true,

    "data":[

    ]
}
```

Used By

* Category Chart
* Category Filter

---

# 9. Search API

## GET /search

Query Parameter

```text
q
```

Purpose

Search disaster events.

The search matches:

* Event Title
* Country
* Category

Response

```json
{
    "success": true,

    "data":[

    ]
}
```

Used By

* Global Search

---

# 10. Timeline API

## GET /timeline

Purpose

Return latest disaster events ordered by time.

Response

```json
{
    "success": true,

    "data":[

    ]
}
```

Used By

* Live Event Feed

---

# 11. Synchronization API

## GET /sync/status

Purpose

Return latest synchronization information.

Response

```json
{
    "success": true,

    "data":{

        "last_sync":"",

        "inserted":0,

        "updated":0,

        "duration":"",

        "status":"Success"

    }
}
```

Used By

* Dashboard Status
* Last Sync Card

---

# 12. API Communication Flow

```text
Dashboard

↓

HTTP Request

↓

Flask Route

↓

Service Layer

↓

MongoDB

↓

Service Layer

↓

JSON Response

↓

Dashboard Update
```

No route performs business logic.

No frontend accesses MongoDB.

---

# 13. HTTP Methods

| Method | Purpose       |
| ------ | ------------- |
| GET    | Retrieve data |

HELIX v1.0 uses only GET endpoints because all data is read-only.

No POST, PUT, PATCH, or DELETE endpoints are required.

---

# 14. Error Handling

Every endpoint must return:

* HTTP Status Code
* JSON Response
* Error Message (if applicable)

Application exceptions must never be exposed to frontend users.

---

# 15. API Design Principles

The REST API follows these principles.

* RESTful Design
* Read-Only Endpoints
* Consistent JSON Structure
* Service Layer Architecture
* Stateless Communication

These API specifications are final for HELIX v1.0.

---

End of Document.
