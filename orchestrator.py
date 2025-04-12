"""
Module for orchestrating the COVID-19 ETL pipeline.
"""
import os
import logging
import time
import pandas as pd
from datetime import datetime, timedelta

# Import project modules
import config
from extractors.csv_extractor import extract_from_csv
from extractors.json_extractor import extract_from_json
from extractors.api_extractor import extract_from_api
from extractors.web_scraper import extract_from_web
from transformers.date_transformer import standardize_dates
from transformers.location_transformer import normalize_locations
from transformers.missing_value_handler import handle_missing_values
from transformers.calculator import create_calculated_fields
from validators.data_validator import validate_covid_data
from loaders.sql_loader import load_to_sqlite, create_database_schema
from loaders.csv_exporter import export_to_csv

logger = logging.getLogger(__name__)

class Task:
    """Simple class to represent an ETL task."""
    
    def __init__(self, name, function, **kwargs):
        """
        Initialize a task.
        
        Args:
            name (str): Task name
            function (callable): Function to execute
            **kwargs: Arguments to pass to the function
        """
        self.name = name
        self.function = function
        self.kwargs = kwargs
        self.result = None
        self.success = None
        self.start_time = None
        self.end_time = None
        self.duration = None
    
    def run(self):
        """Run the task and capture execution metrics."""
        logger.info(f"Starting task: {self.name}")
        self.start_time = time.time()
        
        try:
            self.result = self.function(**self.kwargs)
            self.success = True
            logger.info(f"Task completed successfully: {self.name}")
        except Exception as e:
            self.success = False
            logger.error(f"Task failed: {self.name} - {e}")
            raise
        finally:
            self.end_time = time.time()
            self.duration = self.end_time - self.start_time
            logger.info(f"Task duration: {self.name} - {self.duration:.2f} seconds")
        
        return self.result

def run_pipeline(csv_path=None, json_path=None, api_url=None, html_url=None, export_csv=False):
    """
    Run the complete ETL pipeline.
    
    Args:
        csv_path (str, optional): Path to CSV file
        json_path (str, optional): Path to JSON file
        api_url (str, optional): URL for API endpoint
        html_url (str, optional): URL for web page
        export_csv (bool, optional): Whether to export results to CSV
        
    Returns:
        dict: Dictionary with results of each stage
    """
    logger.info("Starting COVID-19 ETL pipeline")
    results = {}
    
    try:
        # Set default values if not provided
        csv_path = csv_path or config.DEFAULT_CSV_PATH
        json_path = json_path or config.DEFAULT_JSON_PATH
        api_url = api_url or config.DEFAULT_API_URL
        html_url = html_url or config.DEFAULT_HTML_URL
        
        # Extract data
        logger.info("Starting extraction phase")
        
        cases_df = Task("Extract CSV", extract_from_csv, file_path=csv_path).run()
        results['extract_csv'] = cases_df
        
        hospitals_df = Task("Extract JSON", extract_from_json, file_path=json_path).run()
        results['extract_json'] = hospitals_df
        
        vaccinations_df = Task("Extract API", extract_from_api, api_url=api_url).run()
        results['extract_api'] = vaccinations_df
        
        # Optional web scraping
        if html_url:
            web_df = Task("Extract Web", extract_from_web, url=html_url).run()
            results['extract_web'] = web_df
        
        # Transform data
        logger.info("Starting transformation phase")
        
        # Transform cases data
        if not cases_df.empty:
            cases_df = Task("Standardize Dates (Cases)", standardize_dates, df=cases_df, date_columns=config.DATE_FIELDS).run()
            cases_df = Task("Normalize Locations (Cases)", normalize_locations, df=cases_df, location_columns=config.LOCATION_FIELDS).run()
            cases_df = Task("Handle Missing Values (Cases)", handle_missing_values, df=cases_df).run()
            cases_df = Task("Create Calculated Fields (Cases)", create_calculated_fields, df=cases_df).run()
            results['transform_cases'] = cases_df
        
        # Transform hospitals data
        if not hospitals_df.empty:
            hospitals_df = Task("Standardize Dates (Hospitals)", standardize_dates, df=hospitals_df, date_columns=config.DATE_FIELDS).run()
            hospitals_df = Task("Normalize Locations (Hospitals)", normalize_locations, df=hospitals_df, location_columns=config.LOCATION_FIELDS).run()
            hospitals_df = Task("Handle Missing Values (Hospitals)", handle_missing_values, df=hospitals_df).run()
            results['transform_hospitals'] = hospitals_df
        
        # Transform vaccinations data
        if not vaccinations_df.empty:
            vaccinations_df = Task("Standardize Dates (Vaccinations)", standardize_dates, df=vaccinations_df, date_columns=config.DATE_FIELDS).run()
            vaccinations_df = Task("Normalize Locations (Vaccinations)", normalize_locations, df=vaccinations_df, location_columns=config.LOCATION_FIELDS).run()
            vaccinations_df = Task("Handle Missing Values (Vaccinations)", handle_missing_values, df=vaccinations_df).run()
            results['transform_vaccinations'] = vaccinations_df
        
        # Validate data
        logger.info("Starting validation phase")
        
        if not cases_df.empty:
            Task("Validate Cases", validate_covid_data, df=cases_df).run()
        
        if not hospitals_df.empty:
            Task("Validate Hospitals", validate_covid_data, df=hospitals_df).run()
        
        if not vaccinations_df.empty:
            Task("Validate Vaccinations", validate_covid_data, df=vaccinations_df).run()
        
        # Load data to SQLite
        logger.info("Starting loading phase")
        
        # Create database schema
        tables_info = {
            config.CASES_TABLE: [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "date TEXT",
                "region TEXT",
                "confirmed_cases INTEGER",
                "deaths INTEGER",
                "recovered INTEGER",
                "active_cases INTEGER",
                "total_tests INTEGER",
                "positivity_rate REAL",
                "case_fatality_rate REAL"
            ],
            config.HOSPITALS_TABLE: [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "date TEXT",
                "hospital_name TEXT",
                "location TEXT",
                "total_beds INTEGER",
                "occupied_beds INTEGER",
                "available_beds INTEGER",
                "icu_beds INTEGER",
                "ventilators INTEGER",
                "hospital_utilization_rate REAL"
            ],
            config.VACCINATIONS_TABLE: [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "date TEXT",
                "region TEXT",
                "total_vaccinations INTEGER",
                "people_vaccinated INTEGER",
                "people_fully_vaccinated INTEGER",
                "vaccination_rate REAL"
            ]
        }
        
        Task("Create Database Schema", create_database_schema, db_uri=config.DB_URI, tables_info=tables_info).run()
        
        # Load each dataset to SQLite
        if not cases_df.empty:
            Task("Load Cases to SQLite", load_to_sqlite, df=cases_df, table_name=config.CASES_TABLE, db_uri=config.DB_URI).run()
        
        if not hospitals_df.empty:
            Task("Load Hospitals to SQLite", load_to_sqlite, df=hospitals_df, table_name=config.HOSPITALS_TABLE, db_uri=config.DB_URI).run()
        
        if not vaccinations_df.empty:
            Task("Load Vaccinations to SQLite", load_to_sqlite, df=vaccinations_df, table_name=config.VACCINATIONS_TABLE, db_uri=config.DB_URI).run()
        
        # Export to CSV if requested
        if export_csv:
            logger.info("Exporting data to CSV")
            
            if not cases_df.empty:
                export_path = os.path.join(config.DEFAULT_OUTPUT_DIR, "covid_cases.csv")
                Task("Export Cases to CSV", export_to_csv, df=cases_df, file_path=export_path).run()
            
            if not hospitals_df.empty:
                export_path = os.path.join(config.DEFAULT_OUTPUT_DIR, "hospital_resources.csv")
                Task("Export Hospitals to CSV", export_to_csv, df=hospitals_df, file_path=export_path).run()
            
            if not vaccinations_df.empty:
                export_path = os.path.join(config.DEFAULT_OUTPUT_DIR, "vaccinations.csv")
                Task("Export Vaccinations to CSV", export_to_csv, df=vaccinations_df, file_path=export_path).run()
        
        logger.info("COVID-19 ETL pipeline completed successfully")
        return results
    
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

class SimpleScheduler:
    """
    Simple scheduler for running the pipeline at specified intervals.
    """
    
    def __init__(self, interval_minutes=60):
        """
        Initialize the scheduler.
        
        Args:
            interval_minutes (int): Interval between runs in minutes
        """
        self.interval_minutes = interval_minutes
        self.last_run = None
        self.next_run = None
        self.running = False
    
    def start(self, **pipeline_args):
        """
        Start the scheduler.
        
        Args:
            **pipeline_args: Arguments to pass to the pipeline
        """
        logger.info(f"Starting scheduler with {self.interval_minutes} minute interval")
        self.running = True
        
        while self.running:
            # Run the pipeline
            logger.info("Running scheduled pipeline")
            self.last_run = datetime.now()
            
            try:
                run_pipeline(**pipeline_args)
            except Exception as e:
                logger.error(f"Scheduled pipeline run failed: {e}")
            
            # Calculate next run time
            self.next_run = self.last_run + timedelta(minutes=self.interval_minutes)
            sleep_seconds = (self.next_run - datetime.now()).total_seconds()
            
            if sleep_seconds > 0:
                logger.info(f"Next run scheduled for: {self.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"Sleeping for {sleep_seconds:.2f} seconds")
                
                # Sleep in small increments to allow for clean shutdown
                remaining_seconds = sleep_seconds
                while remaining_seconds > 0 and self.running:
                    time.sleep(min(10, remaining_seconds))
                    remaining_seconds -= 10
            else:
                logger.warning("Pipeline took longer than interval, running next iteration immediately")
    
    def stop(self):
        """Stop the scheduler."""
        logger.info("Stopping scheduler")
        self.running = False