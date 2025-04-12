<h1 style="color: #FFFF00;">🦠 COVID-19 ETL Pipeline: User Guide 📊</h1>

<h2 style="color: #ADFF2F;">🔍 Overview</h2>

<p style="color: #FFFFFF;">The COVID-19 ETL (Extract, Transform, Load) pipeline is a robust data processing tool designed to gather COVID-19 data from multiple sources, standardize it, and store it in a centralized SQLite database. This user guide will help you set up and use the pipeline efficiently.</p>

<h2 style="color: #ADFF2F;">📓 Table of Contents</h2>

1. [Installation](#installation)
2. [Data Sources](#data-sources)
3. [Running the Pipeline](#running-the-pipeline)
4. [Command-line Arguments](#command-line-arguments)
5. [Scheduling](#scheduling)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)

<h2 style="color: #ADFF2F;">⚙️ Installation</h2>

<h3 style="color: #FFFF00;">💻 Prerequisites</h3>

- Python 3.8 or higher
- Windows environment (Windows 10/11 recommended)
- Internet connection (for API and web data sources)

<h3 style="color: #FFFF00;">📍 Setup Steps</h3>

1. **Clone or download the project** to your local machine

2. **Install dependencies** using pip:
   ```powershell
   pip install -r requirements.txt
   ```

   > **Note:** The pipeline uses html5lib instead of lxml for HTML parsing to avoid C library dependency issues on Windows systems.

3. **Verify installation** by running a simple test:
   ```powershell
   python main.py --csv_path=".\sample_data\cases.csv" --json_path=".\sample_data\hospitals.json" --html_url="file:///full/path/to/covid19_etl/sample_data/covid_stats.html"
   ```
   
   Replace `full/path/to` with the actual path on your system.

<h2 style="color: #ADFF2F;">📂 Data Sources</h2>

The COVID-19 ETL pipeline extracts data from four different sources:

1. **CSV Files** (COVID-19 case data)
   - Default: `./data/cases.csv`
   - Contains: date, region, confirmed cases, deaths, recoveries, tests, etc.

2. **JSON Files** (Hospital resource data)
   - Default: `./data/hospitals.json`
   - Contains: hospital names, locations, bed capacity, ventilator availability, etc.

3. **API Endpoint** (Vaccination data)
   - Default: CDC COVID-19 Case Surveillance Public Use Data API
   - Contains: vaccination status, demographics, outcomes

4. **Web Pages** (HTML data)
   - Default: CDC COVID-19 Data Tracker
   - Contains: Various COVID-19 statistics

<h3 style="color: #FFFF00;">📁 Sample Data</h3>

Sample data files are included for testing:
- `sample_data/cases.csv`: Sample case data (9 records)
- `sample_data/hospitals.json`: Sample hospital resource data (6 records)
- `sample_data/covid_stats.html`: Sample HTML page with COVID-19 statistics

<h2 style="color: #ADFF2F;">🚀 Running the Pipeline</h2>

<h3 style="color: #FFFF00;">▶️ Basic Execution</h3>

To run the pipeline with default settings:

```powershell
python main.py
```

This uses the default file paths and data sources defined in `config.py`.

<h3 style="color: #FFFF00;">📄 Using Sample Data</h3>

To run with sample data:

```powershell
python main.py --csv_path=".\sample_data\cases.csv" --json_path=".\sample_data\hospitals.json" --html_url="file:///E:/path/to/covid19_etl/sample_data/covid_stats.html"
```

Replace `E:/path/to` with your actual project path.

<h3 style="color: #FFFF00;">📎 Using Local HTML Files</h3>

When using local HTML files, use the `file:///` protocol followed by the **full absolute path**:

```powershell
python main.py --html_url="file:///E:/path/to/covid19_etl/sample_data/covid_stats.html"
```

<h2 style="color: #ADFF2F;">💬 Command-line Arguments</h2>

Customize pipeline execution with these arguments:

| Argument | Description | Default |
|----------|-------------|---------|
| `--csv_path` | Path to CSV file with case data | `./data/cases.csv` |
| `--json_path` | Path to JSON file with hospital data | `./data/hospitals.json` |
| `--api_url` | URL for API with vaccination data | CDC COVID-19 API |
| `--html_url` | URL for web page with COVID-19 data | CDC COVID-19 Data Tracker |
| `--export_csv` | Export results to CSV files | `False` |
| `--schedule` | Run schedule interval in minutes (0 = once) | `0` |

Examples:

```powershell
# Use custom CSV and JSON files
python main.py --csv_path="C:\my_data\cases.csv" --json_path="C:\my_data\hospitals.json"

# Export processed data to CSV
python main.py --export_csv=True

# Use CDC production API
python main.py --api_url="https://data.cdc.gov/resource/vbim-akqf.json"
```

<h3 style="color: #FFFF00;">🔌 Using the Mock API Server</h3>

<p style="color: #FFFFFF;">For testing without internet access or when external APIs are unavailable, the project includes a mock API server that simulates the vaccination data API endpoint. Follow these steps to use it:</p>

<ol style="color: #FFFFFF;">
  <li><strong>Start the mock API server</strong> in a separate PowerShell window:</li>
</ol>

```powershell
python tools/mock_api.py
```

<p style="color: #FFFFFF;">The server will start and listen on <code>http://localhost:8000</code>.</p>

<ol style="color: #FFFFFF;" start="2">
  <li><strong>Run the pipeline</strong> with the mock API:</li>
</ol>

```powershell
python main.py --api_url="http://localhost:8000/covid/vaccinations"
```

<p style="color: #FFFFFF;">This allows you to test the complete pipeline workflow without depending on external API availability.</p>

<h2 style="color: #ADFF2F;">⏰ Scheduling</h2>

To run the pipeline on a regular schedule:

```powershell
python main.py --schedule=60
```

This executes the pipeline every 60 minutes until stopped with Ctrl+C.

The pipeline will:
1. Run immediately upon startup
2. Wait the specified interval (in minutes)
3. Run again
4. Repeat until manually terminated

To run on a continuous schedule with custom data sources:

```powershell
python main.py --schedule=120 --csv_path=".\my_data\cases.csv" --export_csv=True
```

<h2 style="color: #ADFF2F;">📂 Output Files</h2>

<h3 style="color: #FFFF00;">💾 Database Output</h3>

All processed data is stored in a SQLite database:
- Location: `./output/covid19.db`
- Tables:
  - `covid_cases`: Case data from CSV sources
  - `hospital_resources`: Hospital data from JSON sources
  - `vaccinations`: Vaccination data from API sources

<h3 style="color: #FFFF00;">📂 CSV Export (Optional)</h3>

When `--export_csv=True`, processed data is exported to:
- `./output/processed_cases.csv`
- `./output/processed_hospitals.csv`
- `./output/processed_vaccinations.csv`

<h3 style="color: #FFFF00;">📓 Logs</h3>

Pipeline execution logs are stored in:
- Location: `./logs/`
- Format: `etl_YYYYMMDD_HHMMSS.log`

<h2 style="color: #ADFF2F;">🔧 Troubleshooting</h2>

<h3 style="color: #FFFF00;">❓ Common Issues</h3>

1. **HTTP 404 errors from API**
   - The CDC API endpoints may change over time
   - Solution: Check the CDC Open Data Portal for current endpoints

2. **Missing data sources**
   - Error: `File not found: [path]`
   - Solution: Create the default `./data/` directory with required files or specify custom paths

3. **Connection errors**
   - For API and web sources, ensure internet connectivity
   - For local files, verify full paths are correct

4. **Web scraping issues**
   - The pipeline includes fallback data for CDC websites that may change structure
   - Custom HTML sources should have standard table elements

<h3 style="color: #FFFF00;">💬 Getting Help</h3>

Review the log files in the `./logs/` directory for detailed error information.

---

<p style="color: #FFFFFF;">This user guide covers the basic and advanced usage of the COVID-19 ETL pipeline. For technical details about implementation, architecture, and customization, please refer to the <a href="./developers_guide.md" style="color: #00BFFF;">Developer's Guide</a>.</p>
