"""Logging utility for the HELIX application."""

import logging
import sys

def setup_logging() -> None:
    """Sets up the global logging configuration.

    Logs are written to the console in a clear, consistent format.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
