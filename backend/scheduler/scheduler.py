"""Scheduler module for orchestrating Natural Disaster synchronization runs.

Uses APScheduler BackgroundScheduler to run synchronization and aggregation
periodically at the interval loaded from environment configuration.
"""

from datetime import datetime, timezone
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from backend.services.sync_service import sync_events
from backend.services.aggregation import run_aggregation

logger = logging.getLogger(__name__)

# Single instance of BackgroundScheduler
scheduler = BackgroundScheduler()

def execute_sync_pipeline() -> None:
    """Orchestrates the data sync pipeline:

    1. Fetches and persists disaster events.
    2. Regenerates summary collections.
    Continues execution on exceptions to ensure robustness.
    """
    logger.info("Synchronization Started: Beginning scheduled cycle...")
    start_time = datetime.now(timezone.utc)
    
    try:
        # Step 1 & 2 & 3: Fetch, Transform, Upsert events (includes Sync Logging inside sync_service)
        sync_stats = sync_events()
        logger.info("Fetch Completed. Transformation Completed. Database Updated. Stats: %s", sync_stats)
        
        # Step 4: Generate Summary Collections
        run_aggregation()
        logger.info("Aggregation Completed: Summary collections refreshed.")
        
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        logger.info("Synchronization Finished: Cycle completed in %.2fs.", duration)
        
    except Exception as err:
        logger.error("Synchronization Failed: Scheduled cycle encountered error: %s", err)

def start_scheduler() -> None:
    """Starts the background scheduler.

    Configures periodic interval execution based on Config.FETCH_INTERVAL
    and triggers one synchronization run immediately at startup.
    """
    if scheduler.running:
        logger.warning("Scheduler is already running.")
        return

    logger.info("Scheduler Starting...")
    
    # 1. Trigger startup synchronization immediately
    logger.info("Executing startup synchronization immediately...")
    execute_sync_pipeline()
    
    # 2. Schedule periodic execution (interval loaded from Config, interpreted in minutes)
    scheduler.add_job(
        execute_sync_pipeline,
        "interval",
        minutes=Config.FETCH_INTERVAL,
        id="sync_events_job",
        replace_existing=True
    )
    
    # 3. Start the background scheduler
    scheduler.start()
    logger.info("Scheduler Started: Periodic execution scheduled every %d minutes.", Config.FETCH_INTERVAL)
