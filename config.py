"""Configuration loader for the HELIX application.

Loads environment variables from a .env file if it exists, falling back to
default values as specified in the project engineering documents.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration parameters."""
    
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "helix")
    NASA_API_URL: str = os.getenv("NASA_API_URL", "https://eonet.gsfc.nasa.gov/api/v3/events")
    FETCH_INTERVAL: int = int(os.getenv("FETCH_INTERVAL", "60"))
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    
    # Flask configuration
    DEBUG: bool = FLASK_ENV == "development"
    TESTING: bool = FLASK_ENV == "testing"
