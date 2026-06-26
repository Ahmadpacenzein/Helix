# 04_FRONTEND_SPEC.md

---

# HELIX Frontend Specification

Version: 1.0

Status: Approved

Reference

* HELIX_SPEC.md
* 01_SYSTEM_ARCHITECTURE.md
* 03_API_SPECIFICATION.md

---

# 1. Overview

HELIX provides a desktop-first Single Page Dashboard for monitoring global natural disaster events.

The frontend consumes REST APIs provided by the backend and never communicates directly with MongoDB.

The user interface emphasizes readability, responsiveness, and efficient visualization of disaster information.

---

# 2. Design Principles

The dashboard follows the principles below.

* Desktop First
* Single Page Application
* Dark Grey Theme
* Glassmorphism Components
* Minimalist Design
* Responsive Layout
* Smooth Interaction

---

# 3. Theme Specification

## Primary Background

Dark Grey

---

## Cards

Glassmorphism

Blur Background

Rounded Corner

Soft Border

---

## Typography

Primary Text

White

Secondary Text

Light Grey

---

## Accent Colors

Blue

Information

Green

Success

Yellow

Warning

Red

Danger

Colors must be used consistently throughout the application.

---

# 4. Dashboard Layout

```text id="gmy9zb"
+--------------------------------------------------------------+
| Navigation Bar                                                |
+--------------------------------------------------------------+
| Summary Cards                                                 |
+--------------------------------------------------------------+
| Map Area                         | Live Feed + Filter Panel   |
+--------------------------------------------------------------+
| Time Slider                                                |
+--------------------------------------------------------------+
| Analytics Charts                                             |
+--------------------------------------------------------------+
```

The dashboard consists of one page only.

No additional pages are required.

---

# 5. Navigation Bar

Components

* HELIX Logo
* Project Title
* Search Box
* Last Synchronization Status

Purpose

Provide navigation and application status.

---

# 6. Summary Cards

Display

* Total Events
* Active Events
* Total Categories
* Total Countries
* Updated Today

Source

Dashboard API

Cards update automatically after synchronization.

---

# 7. Interactive Map

Technology

MapLibre GL JS

Purpose

Display disaster locations.

Features

* Marker Visualization
* Marker Cluster
* Zoom
* Pan
* Click Marker
* Fly To Location

Data Source

Events API

---

# 8. Event Detail Panel

Display

* Event Title
* Category
* Status
* Country
* Coordinates
* Event Date
* Sources

Data Source

Event Detail API

The panel updates after a marker is selected.

---

# 9. Live Event Feed

Display

Latest disaster events sorted by time.

Maximum Items

20

Data Source

Timeline API

---

# 10. Category Filter

Display

Checkbox list.

Purpose

Filter events displayed on the map.

Data Source

Category Analytics API

---

# 11. Search Component

Purpose

Search events by

* Event Title
* Country
* Category

Data Source

Search API

Search updates the dashboard without reloading the page.

---

# 12. Time Slider

Purpose

Filter disaster events by date.

Data Source

Events API

Interaction

Changing the selected date refreshes:

* Map
* Event Detail
* Live Feed

No page refresh is allowed.

---

# 13. Analytics Section

Contains four visualizations.

## Category Distribution

Chart Type

Pie Chart

Source

Category Analytics API

---

## Country Statistics

Chart Type

Bar Chart

Source

Country Analytics API

---

## Daily Trend

Chart Type

Line Chart

Source

Events API

---

## Synchronization Status

Display

Latest synchronization information.

Source

Synchronization API

---

# 14. Responsive Behavior

Primary Target

Desktop

Minimum Width

1280 pixels

Tablet and mobile responsiveness is secondary and limited to layout adjustment only.

---

# 15. User Interaction Flow

```text id="8kp4ui"
Open Dashboard

↓

Load Dashboard Summary

↓

Load Map

↓

Load Charts

↓

Load Timeline

↓

User Interaction

↓

API Request

↓

Dashboard Update
```

All updates occur asynchronously.

---

# 16. Frontend Architecture

```text id="jlwm9q"
Browser

↓

HTML

↓

Bootstrap Layout

↓

JavaScript

↓

REST API

↓

Backend
```

Frontend never communicates with MongoDB.

---

# 17. JavaScript Modules

The frontend is divided into the following modules.

* app.js
* api.js
* map.js
* dashboard.js
* charts.js
* search.js
* timeline.js

Each module has a single responsibility.

---

# 18. Loading Behavior

During data retrieval:

* Show loading indicator.
* Disable repeated requests.
* Update UI after successful response.
* Display friendly message if data is unavailable.

---

# 19. Error Handling

If an API request fails:

* Display a non-blocking notification.
* Preserve existing dashboard data.
* Allow the user to retry.

Application must remain operational.

---

# 20. Frontend Principles

The frontend follows these principles.

* Desktop First
* Single Page Dashboard
* REST API Communication
* Glassmorphism Design
* Read-Only Interface
* Responsive Layout
* Component-Based JavaScript

These specifications are final for HELIX v1.0.

---

End of Document.
