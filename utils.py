"""
Utility functions for the COVID-19 ETL pipeline.
"""
import os
import logging
import pandas as pd
from datetime import datetime
import dateutil.parser as date_parser
import re

logger = logging.getLogger(__name__)

def ensure_directory(directory_path):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")

def get_dataframe_info(df, name="DataFrame"):
    """Log information about a DataFrame."""
    logger.info(f"{name} shape: {df.shape}")
    logger.info(f"{name} columns: {', '.join(df.columns)}")
    logger.info(f"{name} has null values: {df.isna().any().any()}")

def parse_date_string(date_string):
    """Parse a date string to datetime object."""
    if pd.isna(date_string) or date_string == "":
        return None
    
    try:
        return date_parser.parse(str(date_string))
    except Exception as e:
        logger.error(f"Error parsing date '{date_string}': {e}")
        return None

def standardize_date_format(date_obj, format="%Y-%m-%d"):
    """Convert a datetime object to a standardized string format."""
    if date_obj is None:
        return None
    
    try:
        return date_obj.strftime(format)
    except Exception as e:
        logger.error(f"Error formatting date '{date_obj}': {e}")
        return None

def clean_string(text):
    """Clean and standardize a string value."""
    if pd.isna(text) or text is None:
        return None
    
    # Convert to string, strip whitespace, and convert to lowercase
    return str(text).strip().lower()