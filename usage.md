# COVID-19 ETL Pipeline Usage Guide

This guide explains how to use the COVID-19 ETL pipeline to extract, transform, and load COVID-19 data from multiple sources.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Prepare your data sources:
   - CSV file with case data
   - JSON file with hospital resource data
   - API endpoint for vaccination data
   - (Optional) HTML page with COVID-19 statistics

## Basic Usage

Run the pipeline with default settings:
```
python main.py
```

This will use the default paths defined in `config.py` and perform a single run of the pipeline.

## Customizing Data Sources

You can specify custom data sources using command-line arguments:

```
python main.py --csv_path data/my_cases.csv --json_path data/my_hospitals.json
```

Available arguments:
- `--csv_path`: Path to CSV file with case data
- `--json_path`: Path to JSON file with hospital resource data
- `--api_url`: URL for API endpoint with vaccination data
- `--html_url`: URL for web page with COVID-19 data

## Exporting to CSV

To export the processed data to CSV files:

```
python main.py --export_csv True
```

This will export each dataset to a CSV file in the `output` directory.

## Scheduling

To run the pipeline on a schedule, use the `--schedule` argument with the interval in minutes:

```
python main.py --schedule 60
```

This will run the pipeline every 60 minutes. Press Ctrl+C to stop the scheduled execution.

## Using the Mock API Server

For testing, you can use the included mock API server:

1. Start the mock API server:
   ```
   python tools/mock_api.py
   ```

2. Run the pipeline with the mock API:
   ```
   python main.py --api_url http://localhost:8000/covid/vaccinations
   ```

## Sample Data

The project includes sample data files for testing:
- `sample_data/cases.csv`: Sample case data
- `sample_data/hospitals.json`: Sample hospital resource data
- `sample_data/covid_stats.html`: Sample HTML page with COVID-19 statistics

Use them to test the pipeline:
```
python main.py --csv_path sample_data/cases.csv --json_path sample_data/hospitals.json --html_url file://sample_data/covid_stats.html
```

## Output

The pipeline outputs:
- SQLite database in the `output` directory
- CSV files in the `output` directory (if `--export_csv` is set to `True`)
- Log files in the `logs` directory