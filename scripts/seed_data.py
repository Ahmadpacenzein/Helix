"""Seed script to populate MongoDB with realistic mock data for testing the dashboard."""

from datetime import datetime, timedelta, timezone
from backend.database.mongo import MongoConnection
from backend.services.aggregation import run_aggregation

def seed():
    print("Seeding database with test events...")
    db = MongoConnection.get_db()
    
    # Clear collections
    db.events.delete_many({})
    db.dashboard_summary.delete_many({})
    db.country_summary.delete_many({})
    db.category_summary.delete_many({})
    db.sync_log.delete_many({})

    # Set up 15 realistic mock events
    now = datetime.now(timezone.utc)
    events = [
        {
            "event_id": "EV_001",
            "title": "California Wildfire - Dixie Fire East",
            "description": "Active wildfire in northern California.",
            "category": {"id": "wildfires", "name": "Wildfires"},
            "status": "open",
            "country": "United States",
            "latest_geometry": {"date": (now - timedelta(days=1)).isoformat(), "type": "Point", "latitude": 40.1, "longitude": -121.3},
            "geometry_history": [],
            "sources": [{"id": "CALFIRE", "url": "https://fire.ca.gov"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_002",
            "title": "Alberta Forest Fire - Jasper Region",
            "description": "Out of control forest fire near Jasper National Park.",
            "category": {"id": "wildfires", "name": "Wildfires"},
            "status": "open",
            "country": "Canada",
            "latest_geometry": {"date": now.isoformat(), "type": "Point", "latitude": 52.8, "longitude": -118.0},
            "geometry_history": [],
            "sources": [{"id": "NRCAN", "url": "https://nrcan.gc.ca"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_003",
            "title": "Mount Lewotobi Eruption",
            "description": "Volcanic eruption sending ash plume 2000m high.",
            "category": {"id": "volcanoes", "name": "Volcanoes"},
            "status": "open",
            "country": "Indonesia",
            "latest_geometry": {"date": (now - timedelta(days=2)).isoformat(), "type": "Point", "latitude": -8.53, "longitude": 122.78},
            "geometry_history": [],
            "sources": [{"id": "PVMBG", "url": "https://vsi.esdm.go.id"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_004",
            "title": "Sakurajima Volcanic Activity",
            "description": "Ongoing mild explosive activity at Showa crater.",
            "category": {"id": "volcanoes", "name": "Volcanoes"},
            "status": "closed",
            "country": "Japan",
            "latest_geometry": {"date": (now - timedelta(days=5)).isoformat(), "type": "Point", "latitude": 31.58, "longitude": 130.65},
            "geometry_history": [],
            "sources": [{"id": "JMA", "url": "https://jma.go.jp"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_005",
            "title": "Magnitude 6.8 Earthquake off Valparaiso",
            "description": "Strong offshore earthquake felt in central Chile.",
            "category": {"id": "earthquakes", "name": "Earthquakes"},
            "status": "closed",
            "country": "Chile",
            "latest_geometry": {"date": (now - timedelta(days=3)).isoformat(), "type": "Point", "latitude": -32.9, "longitude": -71.9},
            "geometry_history": [],
            "sources": [{"id": "USGS", "url": "https://usgs.gov"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_006",
            "title": "Kyushu Earthquake - M5.4",
            "description": "Shallow earthquake near Miyazaki prefecture.",
            "category": {"id": "earthquakes", "name": "Earthquakes"},
            "status": "open",
            "country": "Japan",
            "latest_geometry": {"date": (now - timedelta(days=1)).isoformat(), "type": "Point", "latitude": 32.1, "longitude": 131.4},
            "geometry_history": [],
            "sources": [{"id": "USGS", "url": "https://usgs.gov"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_007",
            "title": "Typhoon Ewiniar - Cat 3 Impact",
            "description": "Severe tropical storm making landfall in Luzon.",
            "category": {"id": "severeStorms", "name": "Severe Storms"},
            "status": "open",
            "country": "Philippines",
            "latest_geometry": {"date": now.isoformat(), "type": "Point", "latitude": 14.6, "longitude": 121.0},
            "geometry_history": [],
            "sources": [{"id": "PAGASA", "url": "https://pagasa.dost.gov.ph"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_008",
            "title": "Tornado Outbreak - Oklahoma Plains",
            "description": "Multiple EF-2 tornadoes reported with heavy damage.",
            "category": {"id": "severeStorms", "name": "Severe Storms"},
            "status": "open",
            "country": "United States",
            "latest_geometry": {"date": (now - timedelta(days=1)).isoformat(), "type": "Point", "latitude": 35.4, "longitude": -97.5},
            "geometry_history": [],
            "sources": [{"id": "NOAA", "url": "https://noaa.gov"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_009",
            "title": "Sichuan Basin Flooding",
            "description": "Continuous heavy rainfall leading to river overflows.",
            "category": {"id": "floods", "name": "Floods"},
            "status": "open",
            "country": "China",
            "latest_geometry": {"date": (now - timedelta(days=2)).isoformat(), "type": "Point", "latitude": 30.6, "longitude": 104.0},
            "geometry_history": [],
            "sources": [{"id": "CMA", "url": "https://cma.gov.cn"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_010",
            "title": "Elbe River Basin Flood Alert",
            "description": "Water levels reaching warning tier 3 in Saxony.",
            "category": {"id": "floods", "name": "Floods"},
            "status": "closed",
            "country": "Germany",
            "latest_geometry": {"date": (now - timedelta(days=4)).isoformat(), "type": "Point", "latitude": 51.05, "longitude": 13.73},
            "geometry_history": [],
            "sources": [{"id": "DWD", "url": "https://dwd.de"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_011",
            "title": "Queensland Bushfire - Great Dividing Range",
            "description": "Bushfire threatening rural communities.",
            "category": {"id": "wildfires", "name": "Wildfires"},
            "status": "open",
            "country": "Australia",
            "latest_geometry": {"date": now.isoformat(), "type": "Point", "latitude": -25.2, "longitude": 152.0},
            "geometry_history": [],
            "sources": [{"id": "BOM", "url": "https://bom.gov.au"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_012",
            "title": "Katla Volcanic Tremors",
            "description": "Subglacial seismic activity indicating magma movements.",
            "category": {"id": "volcanoes", "name": "Volcanoes"},
            "status": "open",
            "country": "Iceland",
            "latest_geometry": {"date": (now - timedelta(days=1)).isoformat(), "type": "Point", "latitude": 63.6, "longitude": -19.0},
            "geometry_history": [],
            "sources": [{"id": "IMO", "url": "https://vedur.is"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_013",
            "title": "Gansu Landslide - Heavy Rains",
            "description": "Landslide blocking national highways.",
            "category": {"id": "landslides", "name": "Landslides"},
            "status": "open",
            "country": "China",
            "latest_geometry": {"date": (now - timedelta(days=3)).isoformat(), "type": "Point", "latitude": 36.0, "longitude": 103.8},
            "geometry_history": [],
            "sources": [{"id": "CMA", "url": "https://cma.gov.cn"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_014",
            "title": "Monsoon Flooding in Assam",
            "description": "Widespread flooding affecting 50,000 residents.",
            "category": {"id": "floods", "name": "Floods"},
            "status": "open",
            "country": "India",
            "latest_geometry": {"date": now.isoformat(), "type": "Point", "latitude": 26.2, "longitude": 91.7},
            "geometry_history": [],
            "sources": [{"id": "IMD", "url": "https://mausam.imd.gov.in"}],
            "created_at": now,
            "updated_at": now
        },
        {
            "event_id": "EV_015",
            "title": "Severe Cyclone Remal",
            "description": "Cyclone packing wind speeds of 110 km/h.",
            "category": {"id": "severeStorms", "name": "Severe Storms"},
            "status": "closed",
            "country": "India",
            "latest_geometry": {"date": (now - timedelta(days=6)).isoformat(), "type": "Point", "latitude": 21.9, "longitude": 89.1},
            "geometry_history": [],
            "sources": [{"id": "IMD", "url": "https://mausam.imd.gov.in"}],
            "created_at": now,
            "updated_at": now
        }
    ]

    db.events.insert_many(events)
    
    # Write a success sync log
    db.sync_log.insert_one({
        "last_sync": now.isoformat(),
        "inserted": 15,
        "updated": 0,
        "duration": "1.85s",
        "status": "Success"
    })

    # Run aggregation to update summaries
    run_aggregation()
    print("Seed completed successfully! Inserted 15 events.")

if __name__ == "__main__":
    seed()
