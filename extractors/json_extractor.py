"""
Module for extracting hospital resource data from JSON files.
"""
import os
import json
import logging
import pandas as pd
from utils import get_dataframe_info

logger = logging.getLogger(__name__)

def extract_from_json(file_path):
    """
    Extract hospital resource data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        pandas.DataFrame: DataFrame containing the JSON data
    """
    logger.info(f"Extracting data from JSON file: {file_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"JSON file not found: {file_path}")
            return pd.DataFrame()
        
        # Read JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        else:
            df = pd.json_normalize(data)
        
        # Log dataframe info
        get_dataframe_info(df, name="JSON data")
        
        logger.info(f"Successfully extracted {len(df)} records from JSON")
        return df
    
    except Exception as e:
        logger.error(f"Error extracting data from JSON: {e}")
        return pd.DataFrame()