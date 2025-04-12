"""
Configuration settings for the COVID-19 ETL pipeline.
"""
import os
import logging
from datetime import datetime

# File paths
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# Ensure directories exist
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

# Default file paths
DEFAULT_CSV_PATH = os.path.join(DEFAULT_DATA_DIR, "cases.csv")
DEFAULT_JSON_PATH = os.path.join(DEFAULT_DATA_DIR, "hospitals.json")
DEFAULT_API_URL = "https://api.example.com/covid/vaccinations"
DEFAULT_HTML_URL = "https://example.com/covid/stats"

# Database settings
DB_PATH = os.path.join(DEFAULT_OUTPUT_DIR, "covid19.db")
DB_URI = f"sqlite:///{DB_PATH}"

# Table names
CASES_TABLE = "covid_cases"
HOSPITALS_TABLE = "hospital_resources"
VACCINATIONS_TABLE = "vaccinations"
COMBINED_TABLE = "covid_combined"

# Logging configuration
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Field mappings for standardization
DATE_FIELDS = ["date", "report_date", "vaccination_date", "admission_date"]
LOCATION_FIELDS = ["region", "location", "state", "county", "hospital_location"]