"""
Main entry point for the COVID-19 ETL pipeline.
"""
import os
import logging
import argparse
import signal
import sys

# Import project modules
import config
from orchestrator import run_pipeline, SimpleScheduler

logger = logging.getLogger(__name__)

# Global variable for scheduler instance
scheduler = None

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='COVID-19 ETL Pipeline')
    
    parser.add_argument('--csv_path', type=str, default=None,
                        help='Path to CSV file with case data')
    parser.add_argument('--json_path', type=str, default=None,
                        help='Path to JSON file with hospital resource data')
    parser.add_argument('--api_url', type=str, default=None,
                        help='URL for API endpoint with vaccination data')
    parser.add_argument('--html_url', type=str, default=None,
                        help='URL for web page with COVID-19 data')
    parser.add_argument('--export_csv', type=bool, default=False,
                        help='Export results to CSV files')
    parser.add_argument('--schedule', type=int, default=0,
                        help='Run pipeline on schedule with specified interval in minutes (0 for one-time run)')
    
    return parser.parse_args()

def signal_handler(sig, frame):
    """Handle interrupt signals."""
    logger.info("Received interrupt signal, shutting down...")
    
    if scheduler is not None:
        scheduler.stop()
    
    sys.exit(0)

def main():
    """Main function to run the ETL pipeline."""
    # Register signal handler for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command-line arguments
    args = parse_arguments()
    
    try:
        # Run pipeline once or on schedule
        if args.schedule > 0:
            # Run on schedule
            global scheduler
            scheduler = SimpleScheduler(interval_minutes=args.schedule)
            
            logger.info(f"Running pipeline on schedule every {args.schedule} minutes")
            scheduler.start(
                csv_path=args.csv_path,
                json_path=args.json_path,
                api_url=args.api_url,
                html_url=args.html_url,
                export_csv=args.export_csv
            )
        else:
            # Run once
            logger.info("Running pipeline once")
            run_pipeline(
                csv_path=args.csv_path,
                json_path=args.json_path,
                api_url=args.api_url,
                html_url=args.html_url,
                export_csv=args.export_csv
            )
            
            logger.info("Pipeline run complete")
    
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())