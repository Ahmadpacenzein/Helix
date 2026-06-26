"""Local script to update country names of already stored events and re-aggregate summaries."""

from backend.database.mongo import MongoConnection
from backend.services.transformer import resolve_country
from backend.services.aggregation import run_aggregation

def main():
    print("Fixing country fields for all stored events...")
    db = MongoConnection.get_db()
    collection = db.events
    
    events = list(collection.find({}))
    print(f"Loaded {len(events)} events from MongoDB. Resolving country names...")
    
    updated_count = 0
    for event in events:
        title = event.get("title")
        geom = event.get("latest_geometry", {})
        lat = geom.get("latitude", 0.0)
        lng = geom.get("longitude", 0.0)
        
        resolved = resolve_country(title, lat, lng)
        if resolved != event.get("country"):
            collection.update_one(
                {"event_id": event["event_id"]},
                {"$set": {"country": resolved}}
            )
            updated_count += 1
            
    print(f"Updated country name for {updated_count} events in MongoDB.")
    print("Re-running aggregation pipeline to rebuild analytics collections...")
    run_aggregation()
    print("Fix countries job complete!")

if __name__ == "__main__":
    main()
