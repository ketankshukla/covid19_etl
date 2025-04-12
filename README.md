<h1 style="color: #FFFF00;">🦠 COVID-19 Data Integration ETL Pipeline 📊</h1>

<p style="color: #FFFFFF;">A Python ETL pipeline that integrates COVID-19 data from multiple sources into a unified dataset.</p>

<h2 style="color: #ADFF2F;">📋 Overview</h2>

<p style="color: #FFFFFF;">This project extracts COVID-19 data from:</p>
<ul style="color: #FFFFFF;">
  <li>📄 CSV files containing case data</li>
  <li>🔄 JSON files containing hospital resource data</li>
  <li>🌐 API endpoint for vaccination data (CDC)</li>
  <li>🕸️ Web scraping of HTML tables (optional)</li>
</ul>

<p style="color: #FFFFFF;">The data is transformed to ensure consistency and then loaded into a SQLite database with an option to export to CSV.</p>

<h2 style="color: #ADFF2F;">🗂️ Project Structure</h2>

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

<h2 style="color: #ADFF2F;">⚙️ Installation</h2>

<p style="color: #FFFFFF;">1. Clone this repository</p>
<p style="color: #FFFFFF;">2. Install required packages:</p>

```
pip install -r requirements.txt
```

<h2 style="color: #ADFF2F;">🚀 Usage</h2>

<p style="color: #FFFFFF;">Run the pipeline with default settings:</p>

```
python main.py
```

<p style="color: #FFFFFF;">Run with specific data sources:</p>

```
python main.py --csv_path data/cases.csv --json_path data/hospitals.json
```

<p style="color: #FFFFFF;">Export to CSV after loading to SQLite:</p>

```
python main.py --export_csv True
```

<h3 style="color: #FFFF00;">🔌 Using the Mock API Server</h3>

<p style="color: #FFFFFF;">For testing without internet access or when the CDC API is unavailable, use the included mock API server:</p>

<p style="color: #FFFFFF;">1. Start the mock API server in a separate terminal:</p>

```
python tools/mock_api.py
```

<p style="color: #FFFFFF;">2. Run the pipeline using the mock API:</p>

```
python main.py --api_url http://localhost:8000/covid/vaccinations
```

<h2 style="color: #ADFF2F;">📚 Requirements</h2>

<p style="color: #FFFFFF;">See <code>requirements.txt</code> for a list of required packages.</p>

<h2 style="color: #ADFF2F;">📖 Documentation</h2>

<p style="color: #FFFFFF;">For detailed information about using and developing with this ETL pipeline, please refer to the following guides:</p>

<ul style="color: #FFFFFF;">
  <li>🔍 <a href="./users_guide.md" style="color: #00BFFF;">User's Guide</a> - How to use the ETL pipeline effectively</li>
  <li>💻 <a href="./developers_guide.md" style="color: #00BFFF;">Developer's Guide</a> - Technical details for extending or modifying the pipeline</li>
</ul>

<h2 style="color: #ADFF2F;">🛠️ Issues Fixed</h2>

<p style="color: #FFFFFF;">Recent improvements to the pipeline include:</p>

<ul style="color: #FFFFFF;">
  <li>✅ SQLAlchemy 2.0 compatibility for database operations</li>
  <li>✅ Replaced lxml with html5lib for better Windows compatibility</li>
  <li>✅ Fixed pandas FutureWarning for HTML parsing</li>
  <li>✅ Updated CDC API endpoints for reliable data access</li>
  <li>✅ Added fallback mechanisms for complex web pages</li>
</ul>
