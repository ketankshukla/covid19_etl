"""
Module for extracting vaccination data from API endpoints.
"""
import logging
import requests
import pandas as pd
from utils import get_dataframe_info

logger = logging.getLogger(__name__)

def extract_from_api(api_url, params=None, headers=None):
    """
    Extract vaccination data from an API endpoint.
    
    Args:
        api_url (str): URL of the API endpoint
        params (dict, optional): Query parameters to include in the request
        headers (dict, optional): Headers to include in the request
        
    Returns:
        pandas.DataFrame: DataFrame containing the API data
    """
    logger.info(f"Extracting data from API: {api_url}")
    
    try:
        # Set default values if None
        if params is None:
            # Add CDC-specific parameters for COVID-19 data
            # Limit to 500 records and filter to get vaccination data where possible
            if "data.cdc.gov" in api_url:
                params = {
                    '$limit': 500,
                    '$where': 'vaccination_status IS NOT NULL'
                }
            else:
                params = {}
                
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        
        # Make API request
        response = requests.get(api_url, params=params, headers=headers)
        
        # Check response status
        if response.status_code != 200:
            logger.error(f"API request failed with status code: {response.status_code}")
            return pd.DataFrame()
        
        # Parse JSON response
        data = response.json()
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
            
            # CDC data-specific transformations
            if "data.cdc.gov" in api_url:
                # CDC data requires column renaming for consistency with our schema
                column_mapping = {
                    'case_month': 'date',
                    'state_name': 'region',
                    'current_status': 'status',
                    'sex': 'gender',
                    'age_group': 'age_range'
                }
                
                # Rename columns that exist in the dataframe
                existing_columns = set(df.columns).intersection(set(column_mapping.keys()))
                rename_dict = {col: column_mapping[col] for col in existing_columns}
                df = df.rename(columns=rename_dict)
                
                # Create a combined vaccination_status column if it doesn't exist
                if 'vaccination_status' not in df.columns and 'process_state' in df.columns:
                    df['vaccination_status'] = df['process_state']
        
        elif isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        else:
            df = pd.json_normalize(data)
        
        # Log dataframe info
        get_dataframe_info(df, name="API data")
        
        logger.info(f"Successfully extracted {len(df)} records from API")
        return df
    
    except Exception as e:
        logger.error(f"Error extracting data from API: {e}")
        return pd.DataFrame()