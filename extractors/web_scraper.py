"""
Module for extracting COVID-19 data from web pages by scraping HTML tables.
"""
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import get_dataframe_info

logger = logging.getLogger(__name__)

def extract_from_web(url, table_index=0):
    """
    Extract COVID-19 data from an HTML table on a web page.
    
    Args:
        url (str): URL of the web page containing the HTML table
        table_index (int, optional): Index of the table to extract (default: 0)
        
    Returns:
        pandas.DataFrame: DataFrame containing the extracted table data
    """
    logger.info(f"Extracting data from web page: {url}")
    
    try:
        # Make request to web page
        response = requests.get(url)
        
        # Check response status
        if response.status_code != 200:
            logger.error(f"Web request failed with status code: {response.status_code}")
            return pd.DataFrame()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        
        if not tables:
            logger.error("No tables found on web page")
            return pd.DataFrame()
        
        if table_index >= len(tables):
            logger.error(f"Table index {table_index} out of range, only {len(tables)} tables found")
            return pd.DataFrame()
        
        # Parse table
        df = pd.read_html(str(tables[table_index]))[0]
        
        # Clean column names
        df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
        
        # Log dataframe info
        get_dataframe_info(df, name="Web data")
        
        logger.info(f"Successfully extracted {len(df)} records from web page")
        return df
    
    except Exception as e:
        logger.error(f"Error extracting data from web page: {e}")
        return pd.DataFrame()