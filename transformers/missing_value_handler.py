"""
Module for handling missing values in the COVID-19 data.
"""
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def handle_missing_values(df, strategy="default"):
    """
    Handle missing values in a DataFrame using the specified strategy.
    
    Args:
        df (pandas.DataFrame): DataFrame to transform
        strategy (str): Strategy to handle missing values
                       - "default": Use type-specific defaults
                       - "drop_rows": Drop rows with any missing values
                       - "drop_columns": Drop columns with any missing values
        
    Returns:
        pandas.DataFrame: DataFrame with handled missing values
    """
    logger.info(f"Handling missing values using strategy: {strategy}")
    
    try:
        # Create a copy of the DataFrame to avoid modifying the original
        transformed_df = df.copy()
        
        # Get missing value counts
        missing_counts = transformed_df.isna().sum()
        total_missing = missing_counts.sum()
        
        if total_missing == 0:
            logger.info("No missing values found in DataFrame")
            return transformed_df
        
        logger.info(f"Found {total_missing} missing values across {(missing_counts > 0).sum()} columns")
        
        # Apply strategy
        if strategy == "drop_rows":
            # Drop rows with any missing values
            original_len = len(transformed_df)
            transformed_df = transformed_df.dropna()
            logger.info(f"Dropped {original_len - len(transformed_df)} rows with missing values")
        
        elif strategy == "drop_columns":
            # Drop columns with any missing values
            columns_to_drop = missing_counts[missing_counts > 0].index.tolist()
            transformed_df = transformed_df.drop(columns=columns_to_drop)
            logger.info(f"Dropped {len(columns_to_drop)} columns with missing values: {columns_to_drop}")
        
        else:  # default strategy
            # Apply type-specific defaults
            for column in transformed_df.columns:
                missing_count = missing_counts[column]
                if missing_count > 0:
                    # Apply different strategies based on column data type
                    if pd.api.types.is_numeric_dtype(transformed_df[column]):
                        # Fill numeric columns with 0
                        transformed_df[column] = transformed_df[column].fillna(0)
                        logger.info(f"Filled {missing_count} missing values in numeric column '{column}' with 0")
                    
                    elif pd.api.types.is_datetime64_dtype(transformed_df[column]):
                        # Leave datetime columns as NaT
                        logger.info(f"Left {missing_count} missing values in datetime column '{column}' as NaT")
                    
                    else:
                        # Fill string/object columns with 'Unknown'
                        transformed_df[column] = transformed_df[column].fillna('Unknown')
                        logger.info(f"Filled {missing_count} missing values in column '{column}' with 'Unknown'")
        
        logger.info("Missing value handling completed successfully")
        return transformed_df
    
    except Exception as e:
        logger.error(f"Error handling missing values: {e}")
        return df  # Return original DataFrame on error