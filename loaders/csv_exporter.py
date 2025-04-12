"""
Module for exporting data to CSV files.
"""
import os
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

def export_to_csv(df, file_path=None, output_dir=None, prefix='covid_data'):
    """
    Export DataFrame to a CSV file.
    
    Args:
        df (pandas.DataFrame): DataFrame to export
        file_path (str, optional): Path to the output CSV file
        output_dir (str, optional): Directory for output if file_path not provided
        prefix (str, optional): Filename prefix if file_path not provided
        
    Returns:
        str: Path to the created CSV file, or None if export failed
    """
    try:
        # Check if DataFrame is empty
        if df.empty:
            logger.error("Cannot export empty DataFrame to CSV")
            return None
        
        # Determine the output file path
        if file_path is None:
            # If file_path not provided, create one using timestamp
            if output_dir is None:
                output_dir = os.path.join(os.getcwd(), 'output')
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = os.path.join(output_dir, f"{prefix}_{timestamp}.csv")
        
        # Export DataFrame to CSV
        df.to_csv(file_path, index=False)
        
        logger.info(f"Successfully exported {len(df)} rows to CSV: {file_path}")
        return file_path
    
    except Exception as e:
        logger.error(f"Error exporting data to CSV: {e}")
        return None

def export_query_to_csv(db_uri, query, file_path=None, output_dir=None, prefix='query_result'):
    """
    Export SQL query result to a CSV file.
    
    Args:
        db_uri (str): SQLite database URI
        query (str): SQL query to execute
        file_path (str, optional): Path to the output CSV file
        output_dir (str, optional): Directory for output if file_path not provided
        prefix (str, optional): Filename prefix if file_path not provided
        
    Returns:
        str: Path to the created CSV file, or None if export failed
    """
    try:
        # Create SQLAlchemy engine
        from sqlalchemy import create_engine
        engine = create_engine(db_uri)
        
        # Execute query and get result as DataFrame
        df = pd.read_sql_query(query, engine)
        
        # Check if result is empty
        if df.empty:
            logger.warning("Query result is empty, no CSV exported")
            return None
        
        # Export to CSV
        return export_to_csv(df, file_path, output_dir, prefix)
    
    except Exception as e:
        logger.error(f"Error executing query and exporting to CSV: {e}")
        return None