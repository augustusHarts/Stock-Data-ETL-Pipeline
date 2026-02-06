"""
Global configuration for the Stock Price Pipeline project.

Includes directory paths, API settings, and logging configuration.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Base Directory of the project (3 levels up from this file).
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Directory from storing Raw Data.
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Directory for storing Processed / Structured Data.
DATA_DIR = BASE_DIR / "data" 

# API Configuration
API_TIMEOUT = 10 # Seconds

# Logging
LOG_LEVEL = "INFO" # Logging level: (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Pipeline Configuration
STOCK_SYMBOLS = ['AAPL']

# Yahoo API Parameters
YAHOO_RANGE = '1Y'
YAHOO_INTERVAL = '1d'

ROLLING_WINDOWS = {
    'volatility': 20,
    'ma_20d': 20,
    'ma_50d': 50
}

# Load environment variable
load_dotenv()
db_user = os.getenv('POSTGRES_USER', 'postgres')
db_pass = os.getenv('SQL_PASSWORD')
db_host = os.getenv('DB_HOST', 'postgres')
db_name = os.getenv('POSTGRES_DB', 'stock_pipeline')

if not db_pass:
    raise ValueError(f'Environment variable SQL_PASSWORD not found in .env file.')
DATABASE_URL = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:5432/{db_name}'