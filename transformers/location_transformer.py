"""
Module for normalizing region/location names across all data sources.
"""
import logging
import pandas as pd
from utils import clean_string

logger = logging.getLogger(__name__)

# Simple mapping of location name variations
LOCATION_MAPPING = {
    "ny": "new york",
    "nyc": "new york city",
    "n.y.": "new york",
    "ca": "california",
    "fl": "florida",
    "tx": "texas",
    "pa": "pennsylvania",
    "mass": "massachusetts",
    "ma": "massachusetts",
    "il": "illinois",
    "oh": "ohio",
    "ga": "georgia",
    "nc": "north carolina",
    "nj": "new jersey",
    "wash": "washington",
    "wa": "washington",
    "dc": "district of columbia",
    "d.c.": "district of columbia"
}

def normalize_locations(df, location_columns):
    """
    Normalize location names in a DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame to transform
        location_columns (list): List of column names containing location info
        
    Returns:
        pandas.DataFrame: DataFrame with normalized location names
    """
    logger.info(f"Normalizing location names for columns: {location_columns}")
    
    try:
        # Create a copy of the DataFrame to avoid modifying the original
        transformed_df = df.copy()
        
        # Find actual location columns that exist in the DataFrame
        existing_location_cols = [col for col in location_columns if col in transformed_df.columns]
        
        if not existing_location_cols:
            logger.warning("No location columns found in DataFrame")
            return transformed_df
        
        # Normalize each location column
        for col in existing_location_cols:
            logger.info(f"Normalizing location column: {col}")
            
            # Clean strings and apply mapping
            transformed_df[col] = transformed_df[col].apply(lambda x: clean_location(x))
            
            # Count null values after transformation
            null_count = transformed_df[col].isna().sum()
            if null_count > 0:
                logger.warning(f"Column '{col}' has {null_count} null values after location normalization")
        
        logger.info("Location normalization completed successfully")
        return transformed_df
    
    except Exception as e:
        logger.error(f"Error normalizing locations: {e}")
        return df  # Return original DataFrame on error

def clean_location(location):
    """Clean and normalize a location name."""
    if pd.isna(location) or location is None:
        return None
    
    # Clean the string
    cleaned = clean_string(location)
    
    # Apply mapping if exists
    return LOCATION_MAPPING.get(cleaned, cleaned)