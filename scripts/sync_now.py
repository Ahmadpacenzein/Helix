"""Manual synchronization and aggregation trigger script."""

import sys
from backend.services.sync_service import sync_events
from backend.services.aggregation import run_aggregation

def main():
    print("Manually triggering synchronization run...")
    try:
        stats = sync_events()
        print("Ingestion run completed successfully!")
        print(f"Stats: Total fetched: {stats['total_fetched']}, Inserted: {stats['inserted']}, Updated: {stats['updated']}, Failed: {stats['failed']}")
        
        print("Running aggregation pipeline to refresh summaries...")
        run_aggregation()
        print("Aggregation complete!")
    except Exception as err:
        print(f"Ingestion run failed: {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
