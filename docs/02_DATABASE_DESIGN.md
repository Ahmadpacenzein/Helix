# 02_DATABASE_DESIGN.md

---

# HELIX Database Design

Version: 1.0

Status: Approved

Reference

* HELIX_SPEC.md
* PROJECT_TREE.md
* 01_SYSTEM_ARCHITECTURE.md

---

# 1. Database Overview

HELIX uses MongoDB Community Edition as its primary database.

The database follows a Query-Oriented Data Modeling approach, where document structures are designed based on application query patterns rather than the original NASA API response.

The database consists of five collections.

```text
helix

├── events
├── dashboard_summary
├── country_summary
├── category_summary
└── sync_logs
```

---

# 2. Collection Overview

| Collection        | Purpose                                  |
| ----------------- | ---------------------------------------- |
| events            | Stores all processed disaster events     |
| dashboard_summary | Stores dashboard statistics              |
| country_summary   | Stores aggregated statistics by country  |
| category_summary  | Stores aggregated statistics by category |
| sync_logs         | Stores synchronization history           |

---

# 3. Collection : events

Purpose

Stores every disaster event after transformation.

Each document represents one unique disaster event.

Collection Name

```text
events
```

Primary Key

```text
_id
```

Unique Field

```text
event_id
```

---

## Document Structure

```javascript
{
    _id,

    event_id,

    title,

    description,

    category:{

        id,

        name

    },

    status,

    country,

    latest_geometry:{

        date,

        type,

        latitude,

        longitude

    },

    geometry_history:[

    ],

    sources:[

    ],

    created_at,

    updated_at,

    sync_id
}
```

---

# Embedded Documents

The following objects are embedded.

## category

Reason

Always displayed together with an event.

---

## latest_geometry

Reason

Frequently accessed by dashboard and map.

---

## geometry_history

Reason

Belongs only to one event.

Required for Time Slider.

---

## sources

Reason

Displayed inside Event Detail.

---

# Reference Field

```text
sync_id
```

Reference

```text
sync_logs
```

Purpose

Identify which synchronization process created or updated the event.

---

# 4. Collection : dashboard_summary

Purpose

Provide instant dashboard statistics.

Collection Name

```text
dashboard_summary
```

Document

```javascript
{

    total_events,

    active_events,

    total_categories,

    total_countries,

    updated_today,

    last_sync,

    generated_at

}
```

Purpose

Reduce expensive count operations during dashboard rendering.

---

# 5. Collection : country_summary

Purpose

Store aggregated statistics grouped by country.

Collection Name

```text
country_summary
```

Document

```javascript
{

    country,

    total_events,

    categories:{

    },

    updated_at

}
```

Purpose

Support dashboard map visualization.

Support Top Country chart.

Support country filtering.

---

# 6. Collection : category_summary

Purpose

Store aggregated statistics grouped by disaster category.

Collection Name

```text
category_summary
```

Document

```javascript
{

    category,

    total_events,

    updated_at

}
```

Purpose

Support Pie Chart.

Support Category Filter.

Support Dashboard Statistics.

---

# 7. Collection : sync_logs

Purpose

Store synchronization history.

Collection Name

```text
sync_logs
```

Document

```javascript
{

    sync_id,

    started_at,

    finished_at,

    inserted,

    updated,

    failed,

    duration,

    status

}
```

Purpose

Provide synchronization history.

Display Last Sync information.

Support debugging.

---

# 8. Embedded Document Design

Embedded documents used.

```text
events

├── category
├── latest_geometry
├── geometry_history
└── sources
```

Reason

These objects always belong to one event and are frequently retrieved together.

Embedding reduces lookup operations.

---

# 9. Reference Design

Reference field.

```text
events

↓

sync_id

↓

sync_logs
```

Reason

Synchronization history should remain independent from disaster events.

---

# 10. Denormalization Strategy

HELIX intentionally stores summary collections.

Instead of calculating dashboard statistics every page refresh, aggregation results are stored inside:

* dashboard_summary
* country_summary
* category_summary

Reason

Reduce computation cost.

Improve dashboard loading speed.

Support query optimization.

---

# 11. Index Design

The following indexes must be created.

| Collection | Field                | Type       |
| ---------- | -------------------- | ---------- |
| events     | event_id             | Unique     |
| events     | category.name        | Ascending  |
| events     | country              | Ascending  |
| events     | status               | Ascending  |
| events     | latest_geometry.date | Descending |
| sync_logs  | sync_id              | Unique     |

---

# 12. Query Design

The Events collection supports the following operations.

Search by Event ID

Search by Country

Search by Category

Search by Status

Timeline Query

Time Slider Query

Map Visualization

Event Detail

---

Dashboard Summary Collection supports.

Dashboard Cards

---

Country Summary Collection supports.

Top Countries

Country Statistics

Map Coloring

---

Category Summary Collection supports.

Category Chart

Category Filter

---

Sync Logs Collection supports.

Last Synchronization

Synchronization History

---

# 13. Upsert Strategy

Each synchronization performs:

If Event ID does not exist

↓

Insert

If Event ID exists

↓

Update Existing Document

Duplicate events are not allowed.

---

# 14. Collection Relationship

```text
events
    │
    ├──────────────┐
    │              │
    ▼              ▼
country_summary  category_summary
       │              │
       └──────┬───────┘
              ▼
     dashboard_summary

events
   │
   ▼
sync_logs
```

---

# 15. Database Design Principles

The database follows these principles.

* Query-Oriented Modeling
* Embedded Documents
* Reference Documents
* Denormalization
* Index Optimization
* Aggregation-Based Dashboard

These principles are fixed for HELIX v1.0.

---

End of Document.
