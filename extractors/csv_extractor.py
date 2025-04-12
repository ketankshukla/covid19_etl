"""
Module for extracting COVID-19 case data from CSV files.
"""
import os
import logging
import pandas as pd
from utils import get_dataframe_info

logger = logging.getLogger(__name__)

def extract_from_csv(file_path):
    """
    Extract COVID-19 case data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: DataFrame containing the CSV data
    """
    logger.info(f"Extracting data from CSV file: {file_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"CSV file not found: {file_path}")
            return pd.DataFrame()
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Log dataframe info
        get_dataframe_info(df, name="CSV data")
        
        logger.info(f"Successfully extracted {len(df)} records from CSV")
        return df
    
    except Exception as e:
        logger.error(f"Error extracting data from CSV: {e}")
        return pd.DataFrame()