"""
Module for creating calculated fields from COVID-19 data.
"""
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def create_calculated_fields(df):
    """
    Create calculated fields from COVID-19 data.
    
    Args:
        df (pandas.DataFrame): DataFrame to transform
        
    Returns:
        pandas.DataFrame: DataFrame with calculated fields
    """
    logger.info("Creating calculated fields")
    
    try:
        # Create a copy of the DataFrame to avoid modifying the original
        transformed_df = df.copy()
        
        # Calculate positivity rate if required columns exist
        if 'positive_tests' in transformed_df.columns and 'total_tests' in transformed_df.columns:
            logger.info("Calculating positivity rate")
            transformed_df['positivity_rate'] = (
                transformed_df['positive_tests'] / 
                transformed_df['total_tests'].replace(0, np.nan)  # Avoid division by zero
            ).fillna(0) * 100  # Convert to percentage and handle NaN
            
            logger.info("Positivity rate calculated successfully")
        
        # Calculate case fatality rate if required columns exist
        if 'deaths' in transformed_df.columns and 'confirmed_cases' in transformed_df.columns:
            logger.info("Calculating case fatality rate")
            transformed_df['case_fatality_rate'] = (
                transformed_df['deaths'] / 
                transformed_df['confirmed_cases'].replace(0, np.nan)  # Avoid division by zero
            ).fillna(0) * 100  # Convert to percentage and handle NaN
            
            logger.info("Case fatality rate calculated successfully")
        
        # Calculate vaccination rate if required columns exist
        if 'total_vaccinations' in transformed_df.columns and 'population' in transformed_df.columns:
            logger.info("Calculating vaccination rate")
            transformed_df['vaccination_rate'] = (
                transformed_df['total_vaccinations'] / 
                transformed_df['population'].replace(0, np.nan)  # Avoid division by zero
            ).fillna(0) * 100  # Convert to percentage and handle NaN
            
            logger.info("Vaccination rate calculated successfully")
        
        # Calculate hospital utilization rate if required columns exist
        if 'occupied_beds' in transformed_df.columns and 'total_beds' in transformed_df.columns:
            logger.info("Calculating hospital utilization rate")
            transformed_df['hospital_utilization_rate'] = (
                transformed_df['occupied_beds'] / 
                transformed_df['total_beds'].replace(0, np.nan)  # Avoid division by zero
            ).fillna(0) * 100  # Convert to percentage and handle NaN
            
            logger.info("Hospital utilization rate calculated successfully")
        
        # Log which calculated fields were created
        new_fields = set(transformed_df.columns) - set(df.columns)
        if new_fields:
            logger.info(f"Created {len(new_fields)} new calculated fields: {new_fields}")
        else:
            logger.warning("No calculated fields were created - required columns not found")
        
        return transformed_df
    
    except Exception as e:
        logger.error(f"Error creating calculated fields: {e}")
        return df  # Return original DataFrame on error