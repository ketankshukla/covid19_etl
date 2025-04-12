"""
Module for standardizing date formats across all data sources.
"""
import logging
import pandas as pd
from utils import parse_date_string, standardize_date_format

logger = logging.getLogger(__name__)

def standardize_dates(df, date_columns):
    """
    Standardize date formats in a DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame to transform
        date_columns (list): List of column names containing dates
        
    Returns:
        pandas.DataFrame: DataFrame with standardized dates
    """
    logger.info(f"Standardizing date formats for columns: {date_columns}")
    
    try:
        # Create a copy of the DataFrame to avoid modifying the original
        transformed_df = df.copy()
        
        # Find actual date columns that exist in the DataFrame
        existing_date_cols = [col for col in date_columns if col in transformed_df.columns]
        
        if not existing_date_cols:
            logger.warning("No date columns found in DataFrame")
            return transformed_df
        
        # Standardize each date column
        for col in existing_date_cols:
            logger.info(f"Standardizing date column: {col}")
            
            # Parse dates and standardize format
            transformed_df[col] = transformed_df[col].apply(
                lambda x: standardize_date_format(parse_date_string(x))
            )
            
            # Count null values after transformation
            null_count = transformed_df[col].isna().sum()
            if null_count > 0:
                logger.warning(f"Column '{col}' has {null_count} null values after date standardization")
        
        logger.info("Date standardization completed successfully")
        return transformed_df
    
    except Exception as e:
        logger.error(f"Error standardizing dates: {e}")
        return df  # Return original DataFrame on error