"""
ETL Pipeline - Sales Data Processing
Author: Surendhar Jagannathan
Purpose: Extract, transform, and load sales data from multiple sources
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

# Create output folder if it doesn't exist
os.makedirs('../output', exist_ok=True)

print("=" * 60)
print("ETL PIPELINE - SALES DATA PROCESSING")
print("=" * 60)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ==========================================
# STEP 1: EXTRACT - Read data from CSV files
# ==========================================

print("[STEP 1] EXTRACT: Reading data from CSV files...")
print("-" * 40)

# Read sales data
sales_df = pd.read_csv('../extract/sales_data.csv')
print(f"  ✓ Sales data: {len(sales_df)} rows loaded")

# Read products data
products_df = pd.read_csv('../extract/products.csv')
print(f"  ✓ Products data: {len(products_df)} rows loaded")

# Read customers data
customers_df = pd.read_csv('../extract/customers.csv')
print(f"  ✓ Customers data: {len(customers_df)} rows loaded")

print()

# ==========================================
# STEP 2: TRANSFORM - Clean and process data
# ==========================================

print("[STEP 2] TRANSFORM: Cleaning and processing data...")
print("-" * 40)

# 2.1 Create Total column
sales_df['Total'] = sales_df['Quantity'] * sales_df['UnitPrice']
print(f"  ✓ Created 'Total' column (Quantity × UnitPrice)")

# 2.2 Remove duplicates
initial_rows = len(sales_df)
sales_df = sales_df.drop_duplicates()
print(f"  ✓ Removed {initial_rows - len(sales_df)} duplicate rows")

# 2.3 Handle missing values
sales_df = sales_df.fillna({'Quantity': 0, 'UnitPrice': 0})
print(f"  ✓ Handled missing values")

# 2.4 Convert OrderDate to datetime
sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'])
print(f"  ✓ Converted OrderDate to datetime format")

# 2.5 Extract month and year
sales_df['Month'] = sales_df['OrderDate'].dt.month
sales_df['Year'] = sales_df['OrderDate'].dt.year
print(f"  ✓ Extracted Month and Year from OrderDate")

# 2.6 Merge with products
sales_df = sales_df.merge(products_df, on='ProductID', how='left')
print(f"  ✓ Merged with products data")

# 2.7 Merge with customers
sales_df = sales_df.merge(customers_df, on='CustomerID', how='left')
print(f"  ✓ Merged with customers data")

# 2.8 Create region summary
region_summary = sales_df.groupby('Region').agg({
    'Total': 'sum',
    'Quantity': 'sum',
    'OrderID': 'count'
}).rename(columns={'OrderID': 'OrderCount'}).reset_index()
print(f"  ✓ Created region summary")

# 2.9 Create product summary
product_summary = sales_df.groupby('ProductName').agg({
    'Total': 'sum',
    'Quantity': 'sum',
    'OrderID': 'count'
}).rename(columns={'OrderID': 'OrderCount'}).reset_index()
print(f"  ✓ Created product summary")

print()

# ==========================================
# STEP 3: LOAD - Save to database and Excel
# ==========================================

print("[STEP 3] LOAD: Saving to destinations...")
print("-" * 40)

# 3.1 Save to SQLite database
conn = sqlite3.connect('../output/sales_database.db')

sales_df.to_sql('sales_data', conn, if_exists='replace', index=False)
region_summary.to_sql('region_summary', conn, if_exists='replace', index=False)
product_summary.to_sql('product_summary', conn, if_exists='replace', index=False)

conn.close()
print(f"  ✓ Data loaded to SQLite database: output/sales_database.db")

# 3.2 Export to Excel
with pd.ExcelWriter('../output/cleaned_sales_data.xlsx', engine='openpyxl') as writer:
    sales_df.to_excel(writer, sheet_name='Sales Data', index=False)
    region_summary.to_excel(writer, sheet_name='Region Summary', index=False)
    product_summary.to_excel(writer, sheet_name='Product Summary', index=False)
print(f"  ✓ Data exported to Excel: output/cleaned_sales_data.xlsx")

# 3.3 Export region summary as CSV
region_summary.to_csv('../output/region_summary.csv', index=False)
print(f"  ✓ Region summary saved as CSV: output/region_summary.csv")

print()

# ==========================================
# STEP 4: VALIDATION - Show summary statistics
# ==========================================

print("[STEP 4] VALIDATION: Pipeline summary")
print("=" * 60)

print(f"\n📊 DATA QUALITY REPORT:")
print(f"   Total records processed: {len(sales_df)}")
print(f"   Total columns: {len(sales_df.columns)}")
print(f"   Date range: {sales_df['OrderDate'].min().date()} to {sales_df['OrderDate'].max().date()}")

print(f"\n💰 FINANCIAL SUMMARY:")
print(f"   Total Sales: £{sales_df['Total'].sum():,.2f}")
print(f"   Average Order Value: £{sales_df['Total'].mean():,.2f}")
print(f"   Highest Order: £{sales_df['Total'].max():,.2f}")
print(f"   Lowest Order: £{sales_df['Total'].min():,.2f}")

print(f"\n🏆 TOP PERFORMING REGION:")
top_region = region_summary.loc[region_summary['Total'].idxmax()]
print(f"   {top_region['Region']}: £{top_region['Total']:,.2f} ({top_region['OrderCount']} orders)")

print(f"\n🏆 TOP SELLING PRODUCT:")
top_product = product_summary.loc[product_summary['Total'].idxmax()]
print(f"   {top_product['ProductName']}: £{top_product['Total']:,.2f} ({top_product['OrderCount']} orders)")

print("\n" + "=" * 60)
print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)