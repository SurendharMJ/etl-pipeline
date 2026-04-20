# ETL Pipeline - Sales Data Processing

## Project Overview
End-to-end ETL pipeline that extracts sales data from multiple CSV files, transforms it (cleaning, merging, aggregating), and loads it to SQLite database and Excel.

## Pipeline Architecture

## Skills Demonstrated

| Category | Skills |
| :--- | :--- |
| **Extract** | Reading multiple CSV files, handling different formats |
| **Transform** | Data cleaning, merging, aggregation, date parsing, column creation |
| **Load** | SQLite database, Excel export, CSV export |
| **Python** | Pandas, SQLite3, OS, Datetime |

## Key Metrics

| Metric | Value |
| :--- | :--- |
| Total Sales | £1,135 |
| Average Order | £75.67 |
| Top Region | North (£300) |
| Top Product | Mechanical Keyboard (£450) |

## Output Files

| File | Description |
| :--- | :--- |
| `sales_database.db` | SQLite database with 3 tables |
| `cleaned_sales_data.xlsx` | Excel with Sales, Region, Product sheets |
| `region_summary.csv` | Region-wise sales summary |

## How to Run

```bash
pip install pandas openpyxl
cd scripts
python etl_pipeline.py
