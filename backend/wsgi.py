"""
WSGI entry point for production deployment
"""

import os
import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from backend.main import app
from config import Config

if not Config.validate_data_files():
    print("Data files validation failed. Please run data preparation scripts.")
    sys.exit(1)

if __name__ == "__main__":
    app.run()