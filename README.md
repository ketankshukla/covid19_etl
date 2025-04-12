# COVID-19 Data Integration ETL Pipeline

A Python ETL pipeline that integrates COVID-19 data from multiple sources into a unified dataset.

## Overview

This project extracts COVID-19 data from:
- CSV files containing case data
- JSON files containing hospital resource data
- API endpoint for vaccination data
- Optional web scraping of HTML tables

The data is transformed to ensure consistency and then loaded into a SQLite database with an option to export to CSV.

## Project Structure

```
covid19_etl/
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── extractors/
│   ├── __init__.py
│   ├── csv_extractor.py   # Extract from CSV files
│   ├── json_extractor.py  # Extract from JSON files
│   ├── api_extractor.py   # Extract from API endpoints
│   └── web_scraper.py     # Extract from web pages
├── transformers/
│   ├── __init__.py
│   ├── date_transformer.py       # Standardize dates
│   ├── location_transformer.py   # Normalize locations
│   ├── missing_value_handler.py  # Handle missing values
│   └── calculator.py             # Create calculated fields
├── validators/
│   ├── __init__.py
│   └── data_validator.py  # Validate data quality
├── loaders/
│   ├── __init__.py
│   ├── sql_loader.py      # Load to SQLite
│   └── csv_exporter.py    # Export to CSV
├── orchestrator.py        # Pipeline orchestration
└── main.py                # Main entry point
```

## Installation

1. Clone this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the pipeline with default settings:
```
python main.py
```

Run with specific data sources:
```
python main.py --csv_path data/cases.csv --json_path data/hospitals.json
```

Export to CSV after loading to SQLite:
```
python main.py --export_csv True
```

## Requirements

See `requirements.txt` for a list of required packages.
