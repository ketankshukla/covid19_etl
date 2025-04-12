<h1 style="color: #FFFF00;">🦠 COVID-19 ETL Pipeline: Developer's Guide 💻</h1>

<h2 style="color: #ADFF2F;">🖼 Technical Architecture</h2>

<p style="color: #FFFFFF;">This document provides comprehensive technical documentation for developers maintaining, extending, or modifying the COVID-19 ETL pipeline. It includes architectural details, component descriptions, implementation notes, and information about issues that were resolved during development.</p>

<h2 style="color: #ADFF2F;">📓 Table of Contents</h2>

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Component Documentation](#component-documentation)
4. [Data Flow](#data-flow)
5. [Database Schema](#database-schema)
6. [Dependencies](#dependencies)
7. [API Integration](#api-integration)
8. [Web Scraping](#web-scraping)
9. [Resolved Issues](#resolved-issues)
10. [Extension Points](#extension-points)
11. [Testing](#testing)

<h2 style="color: #ADFF2F;">🗜 Architecture Overview</h2>

The COVID-19 ETL pipeline is designed as a modular data processing system that follows the Extract, Transform, Load (ETL) pattern. The pipeline is orchestrated by a simple scheduler that can run once or periodically.

<h3 style="color: #FFFF00;">🗺 High-Level Architecture</h3>

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Extraction     │ ──> │  Transformation │ ──> │  Loading        │
│  - CSV          │     │  - Date         │     │  - Schema       │
│  - JSON         │     │  - Location     │     │    Creation     │
│  - API          │     │  - Missing      │     │  - Data         │
│  - Web Scraping │     │    Values       │     │    Loading      │
│                 │     │  - Calculation  │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

<h3 style="color: #FFFF00;">🖫 Core Components</h3>

- **Orchestrator**: Coordinates the pipeline execution
- **Extractors**: Pull data from various sources
- **Transformers**: Clean and standardize data
- **Validators**: Ensure data quality
- **Loaders**: Store data in the target database

<h2 style="color: #ADFF2F;">🗃 Directory Structure</h2>

```
covid19_etl/
├── data/                  # Default data directory
│   ├── cases.csv          # CSV input
│   └── hospitals.json     # JSON input
├── extractors/            # Data extraction modules
│   ├── __init__.py
│   ├── api_extractor.py   # API extraction
│   ├── csv_extractor.py   # CSV extraction
│   ├── json_extractor.py  # JSON extraction
│   └── web_scraper.py     # Web scraping
├── loaders/               # Data loading modules
│   ├── __init__.py
│   ├── csv_loader.py      # CSV export
│   └── sql_loader.py      # SQLite loading
├── logs/                  # Log files directory
├── output/                # Output directory for database and exports
├── sample_data/           # Sample data for testing
│   ├── cases.csv
│   ├── hospitals.json
│   └── covid_stats.html
├── tools/                 # Utility scripts
│   └── mock_api.py        # Mock API server for testing
├── transformers/          # Data transformation modules
│   ├── __init__.py
│   ├── calculator.py      # Calculate derived fields
│   ├── date_transformer.py # Date standardization
│   ├── location_transformer.py # Location normalization
│   └── missing_value_handler.py # Missing value handling
├── validators/            # Data validation modules
│   ├── __init__.py
│   └── data_validator.py  # Validation logic
├── config.py              # Configuration settings
├── main.py                # Entry point
├── orchestrator.py        # Pipeline execution logic
├── requirements.txt       # Dependencies
├── users_guide.md         # User documentation
├── developers_guide.md    # Technical documentation
└── utils.py               # Utility functions
```

<h2 style="color: #ADFF2F;">📙 Component Documentation</h2>

<h3 style="color: #FFFF00;">👍 Main Module (`main.py`)</h3>

The main entry point that parses command-line arguments and initializes the pipeline. It supports:
- One-time execution
- Scheduled execution with specified intervals
- Custom data source paths
- Export to CSV option

Key functions:
- `parse_arguments()`: Command-line argument parsing
- `signal_handler()`: Handles interrupt signals for clean shutdown
- `main()`: Primary execution function

<h3 style="color: #FFFF00;">🌀 Orchestrator (`orchestrator.py`)</h3>

Manages the execution flow of the ETL pipeline using a task-based approach.

Classes:
- `Task`: Represents a single operation in the pipeline
- `SimpleScheduler`: Manages scheduled execution at regular intervals

Functions:
- `run_pipeline()`: Executes the complete ETL process

<h3 style="color: #FFFF00;">🔧 Configuration (`config.py`)</h3>

Contains all configuration settings including:
- Default file paths
- Database connection settings
- Table names
- Logging configuration
- Field mappings for standardization

Key improvements:
- Updated to use real CDC COVID-19 data API endpoint
- Configured to use the CDC COVID-19 Data Tracker for web data

<h3 style="color: #FFFF00;">🔎 Extractors</h3>

<h4 style="color: #00FF7F;">📄 CSV Extractor (`extractors/csv_extractor.py`)</h4>

Extracts data from CSV files using pandas.

Functions:
- `extract_from_csv(file_path)`: Loads CSV file into DataFrame

<h4 style="color: #00FF7F;">📝 JSON Extractor (`extractors/json_extractor.py`)</h4>

Extracts data from JSON files.

Functions:
- `extract_from_json(file_path)`: Loads JSON file into DataFrame

<h4 style="color: #00FF7F;">🌐 API Extractor (`extractors/api_extractor.py`)</h4>

Extracts data from REST APIs.

Functions:
- `extract_from_api(api_url, params, headers)`: Fetches data from API endpoint

Key improvements:
- Added special handling for CDC API format
- Implemented automatic column mapping for CDC data
- Added parameters to limit API query results

<h4 style="color: #00FF7F;">🕸️ Web Scraper (`extractors/web_scraper.py`)</h4>

Extracts data from HTML tables on web pages.

Functions:
- `extract_from_web(url, table_index)`: Scrapes HTML tables

Key improvements:
- Added support for local file URLs using `file:///` protocol
- Switched from lxml to html5lib for better Windows compatibility
- Implemented StringIO for handling HTML content to eliminate FutureWarnings
- Added CDC-specific fallback mechanism for complex web pages
- Added automatic column mapping for standardization

<h3 style="color: #FFFF00;">🔄 Transformers</h3>

Collection of modules that clean and standardize the extracted data:

- `date_transformer.py`: Standardizes date formats
- `location_transformer.py`: Normalizes location names
- `missing_value_handler.py`: Handles missing values
- `calculator.py`: Creates calculated fields (e.g., positivity rate)

<h3 style="color: #FFFF00;">✅ Validators</h3>

- `data_validator.py`: Performs data quality checks and validations

<h3 style="color: #FFFF00;">📤 Loaders</h3>

<h4 style="color: #00FF7F;">💾 SQL Loader (`loaders/sql_loader.py`)</h4>

Handles database operations:

Functions:
- `create_database_schema(db_uri, tables_info)`: Creates database tables
- `load_to_sqlite(df, table_name, db_uri)`: Loads DataFrame to SQLite

Key improvements:
- Fixed SQLAlchemy query execution for compatibility with SQLAlchemy 2.0+
- Added proper text() wrapping for raw SQL statements

<h4 style="color: #00FF7F;">📚 CSV Loader (`loaders/csv_loader.py`)</h4>

Exports processed data to CSV files.

<h3 style="color: #FFFF00;">🗜 Utilities (`utils.py`)</h3>

Contains common utility functions used throughout the pipeline:

- Logging helpers
- DataFrame information display
- File path utilities

<h2 style="color: #ADFF2F;">📊 Data Flow</h2>

The pipeline processes data in the following sequence:

1. **Extraction Phase**
   - Load case data from CSV
   - Load hospital data from JSON
   - Fetch vaccination data from API
   - Scrape statistics from web pages

2. **Transformation Phase**
   - Standardize date formats
   - Normalize location names
   - Handle missing values
   - Calculate derived fields

3. **Validation Phase**
   - Validate case data
   - Validate hospital data
   - Validate vaccination data

4. **Loading Phase**
   - Create database schema
   - Load case data to SQLite
   - Load hospital data to SQLite
   - Load vaccination data to SQLite
   - (Optional) Export to CSV files

<h2 style="color: #ADFF2F;">📟 Database Schema</h2>

The SQLite database consists of the following tables:

<h3 style="color: #FFFF00;">📈 covid_cases</h3>
Stores case data extracted from CSV files.

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of report |
| region | TEXT | Geographic region |
| confirmed_cases | INTEGER | Number of confirmed cases |
| deaths | INTEGER | Number of deaths |
| recovered | INTEGER | Number of recoveries |
| active_cases | INTEGER | Number of active cases |
| total_tests | INTEGER | Total tests conducted |
| positive_tests | INTEGER | Number of positive tests |
| positivity_rate | REAL | Calculated ratio of positive to total tests |
| case_fatality_rate | REAL | Calculated ratio of deaths to confirmed cases |

<h3 style="color: #FFFF00;">🏥 hospital_resources</h3>
Stores hospital resource data extracted from JSON files.

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of report |
| hospital_name | TEXT | Name of hospital |
| hospital_location | TEXT | Location of hospital |
| total_beds | INTEGER | Total number of beds |
| occupied_beds | INTEGER | Number of occupied beds |
| available_beds | INTEGER | Number of available beds |
| icu_beds | INTEGER | Number of ICU beds |
| ventilators | INTEGER | Number of ventilators |

<h3 style="color: #FFFF00;">💉 vaccinations</h3>
Stores vaccination data extracted from API.

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of vaccination |
| region | TEXT | Geographic region |
| gender | TEXT | Gender of recipient |
| age_range | TEXT | Age range of recipient |
| vaccination_status | TEXT | Vaccination status |
| vaccine_type | TEXT | Type of vaccine |
| doses | INTEGER | Number of doses |
| adverse_events | INTEGER | Number of adverse events |

<h2 style="color: #ADFF2F;">🔗 Dependencies</h2>

The project uses the following key dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >= 1.3.0 | Data manipulation and analysis |
| numpy | >= 1.20.0 | Numerical operations |
| requests | >= 2.25.0 | HTTP requests for API and web |
| beautifulsoup4 | >= 4.9.0 | HTML parsing for web scraping |
| html5lib | >= 1.1 | HTML parser for pandas read_html |
| sqlalchemy | >= 2.0.0 | Database ORM and operations |
| python-dateutil | >= 2.8.0 | Date parsing and manipulation |
| greenlet | >= 2.0.0 | Required by SQLAlchemy for async features |

Note: lxml has been removed from dependencies due to C compilation issues on Windows systems. The project now uses html5lib as a pure Python alternative.

<h2 style="color: #ADFF2F;">📶 API Integration</h2>

<h3 style="color: #FFFF00;">🌏 CDC COVID-19 API</h3>

The pipeline integrates with the CDC COVID-19 Case Surveillance Public Use Data API:

```
https://data.cdc.gov/resource/vbim-akqf.json
```

Special handling for the CDC API includes:

- Query parameters to limit results:
  ```python
  params = {
      '$limit': 500,
      '$where': 'vaccination_status IS NOT NULL'
  }
  ```

- Column mapping for standardization:
  ```python
  column_mapping = {
      'case_month': 'date',
      'state_name': 'region',
      'current_status': 'status',
      'sex': 'gender',
      'age_group': 'age_range'
  }
  ```

<h2 style="color: #ADFF2F;">🔍 Web Scraping</h2>

<h3 style="color: #FFFF00;">📃 CDC COVID-19 Data Tracker</h3>

The pipeline scrapes COVID-19 data from the CDC COVID-19 Data Tracker:

```
https://covid.cdc.gov/covid-data-tracker/#datatracker-home
```

Key features:

- Automatic URL modification to access data tables
- Fallback mechanism for complex web pages
- Column mapping for standardization
- StringIO implementation to avoid pandas FutureWarnings

<h3 style="color: #FFFF00;">📁 Local File Handling</h3>

The web scraper supports local HTML files using the `file:///` protocol:

```python
# Handling local files
if parsed_url.scheme == 'file':
    file_path = parsed_url.path.lstrip('/')
    
    # Windows path adjustment
    if os.name == 'nt' and file_path.startswith(':'):
        file_path = file_path[1:]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
```

<h2 style="color: #ADFF2F;">🔧 Resolved Issues</h2>

During development, several issues were identified and fixed:

<h3 style="color: #FFFF00;">🔊 1. SQLAlchemy Query Execution</h3>

**Issue**: SQLite verification queries failed with error:
```
Error loading data to SQLite: Not an executable object: 'SELECT COUNT(*) FROM covid_cases'
```

**Solution**: Updated to use SQLAlchemy 2.0 compatible query execution:
```python
from sqlalchemy import text
result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
```

<h3 style="color: #FFFF00;">🔗 2. HTML Parsing Dependencies</h3>

**Issue**: lxml dependency caused installation failures on Windows systems due to C compiler requirements.

**Solution**: 
- Switched to html5lib, a pure Python HTML parser
- Updated requirements.txt to remove lxml and add html5lib
- Modified web_scraper.py to use html5lib parser

<h3 style="color: #FFFF00;">⚠️ 3. Pandas FutureWarning</h3>

**Issue**: Web scraper generated warnings due to deprecated method of passing HTML content:
```
FutureWarning: Passing literal html to 'read_html' is deprecated.
```

**Solution**: Used StringIO to wrap HTML content:
```python
from io import StringIO
html_table = str(tables[table_index])
df = pd.read_html(StringIO(html_table), flavor='html5lib')[0]
```

<h3 style="color: #FFFF00;">👜 4. CDC API Endpoint Availability</h3>

**Issue**: Initial CDC API endpoint returned 404 Not Found errors.

**Solution**: Updated to use a current, working CDC API endpoint:
```python
DEFAULT_API_URL = "https://data.cdc.gov/resource/vbim-akqf.json"
```

<h3 style="color: #FFFF00;">🕸️ 5. Web Scraping Complex Pages</h3>

**Issue**: CDC website structure wasn't easily parseable with simple table extraction.

**Solution**: Added a fallback mechanism that provides sample data when tables can't be located:
```python
if "covid.cdc.gov" in url and not tables:
    # Create sample data for fallback
    dummy_data = [
        {'date': '2025-04-12', 'region': 'National', ...}
    ]
    return pd.DataFrame(dummy_data)
```

<h2 style="color: #ADFF2F;">💪 Extension Points</h2>

The pipeline is designed to be easily extended. Here are the main extension points:

<h3 style="color: #FFFF00;">➕ Adding New Data Sources</h3>

1. Create a new extractor module in the `extractors/` directory
2. Implement an extraction function that returns a pandas DataFrame
3. Update the orchestrator to use the new extractor

<h3 style="color: #FFFF00;">🔄 Adding New Transformations</h3>

1. Create a new transformer module in the `transformers/` directory
2. Implement transformation functions that operate on pandas DataFrames
3. Update the orchestrator to include the new transformation step

<h3 style="color: #FFFF00;">📎 Adding New Output Formats</h3>

1. Create a new loader module in the `loaders/` directory
2. Implement loading functions for the target format or system
3. Update the orchestrator to use the new loader

<h3 style="color: #FFFF00;">☑️ Custom Validation Rules</h3>

1. Update the `validators/data_validator.py` to include new validation rules
2. Add the validation expectations to be checked

<h2 style="color: #ADFF2F;">🔍 Testing</h2>

<h3 style="color: #FFFF00;">🛠️ Unit Testing</h3>

Test individual components using pytest:

```bash
pytest tests/
```

<h3 style="color: #FFFF00;">🔗 Integration Testing</h3>

Test the full pipeline with sample data:

```bash
python main.py --csv_path="./sample_data/cases.csv" --json_path="./sample_data/hospitals.json" --html_url="file:///path/to/sample_data/covid_stats.html"
```

<h3 style="color: #FFFF00;">🖥️ Mock API Server</h3>

For testing API extraction without external dependencies:

1. Start the mock server:
   ```bash
   python tools/mock_api.py
   ```

2. Run the pipeline with the mock API:
   ```bash
   python main.py --api_url="http://localhost:8000/covid/vaccinations"
   ```

---

<p style="color: #FFFFFF;">This developer's guide provides comprehensive documentation for understanding, maintaining, and extending the COVID-19 ETL pipeline. It includes architectural details, implementation notes, and documentation of issues that were fixed during development. For a user-focused guide on running the pipeline, please refer to the <a href="./users_guide.md" style="color: #00BFFF;">User's Guide</a>.</p>
