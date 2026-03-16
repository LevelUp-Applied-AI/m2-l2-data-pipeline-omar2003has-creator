"""
Lab 2 — Data Pipeline: Retail Sales Analysis
Module 2 — Programming for AI & Data Science

Complete each function below. Remove the TODO: comments and pass statements
as you implement each function. Do not change the function signatures.
"""

from ast import Load
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH = 'data/sales_records.csv'
OUTPUT_DIR = 'output'


# ─── Pipeline Functions ───────────────────────────────────────────────────────

def load_data(filepath):
     
                

            sales_data=pd .read_csv(filepath)    
            print(f"Loaded {len(sales_data)} records from {filepath}")
            return sales_data


def clean_data(df) :
   """Handle missing values and fix data types. Returns a cleaned DataFrame."""
   df = df.copy()
    
    # Fill missing 'quantity' values with the column median
   df['quantity'] = df['quantity'].fillna(df['quantity'].median())
    
     # Fill missing 'unit_price' values with the column median
   df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    
    # Parse 'date' to datetime using pd.to_datetime with errors='coerce'
   df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
    
    # Handle NaT values explicitly (drop rows with invalid dates)
   df = df.dropna(subset=['date'])
    
    # Drop rows where BOTH quantity AND unit_price are still missing after fill
   df = df.dropna(subset=['quantity', 'unit_price'], how='all')
    
    # Print: "Cleaned data: N records"
   print(f"Cleaned data: {len(df)} records")
    
    # Return the cleaned DataFrame
   return df

def add_features(df):
    """Compute derived columns.

    - Add 'revenue' column: quantity * unit_price.
    - Add 'day_of_week' column: day name from the date column.

    Args:
        df (pd.DataFrame): Cleaned DataFrame from clean_data().

    Returns:
        pd.DataFrame: DataFrame with new columns added.
    """
    df = df.copy()
    df['revenue'] = df['quantity'] * df['unit_price']
    df['day_of_week'] = df['date'].dt.day_name()
    print(f" Sample of the Featured data : \n {df.head()}")
    return df


def generate_summary(df):
        
    summary = {
        'total_revenue': df['revenue'].sum(),
        'avg_order_value': df['revenue'].mean(),
        'top_category': df.groupby('product_category')['revenue'].sum().idxmax(),
        'record_count': len(df)
    }
    
    return summary
    


def create_visualizations(df, output_dir=OUTPUT_DIR):
    """Create and save 3 charts as PNG files """
    os.makedirs(output_dir, exist_ok=True)

    revenue_by_category = df.groupby('product_category')['revenue'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(revenue_by_category.index, revenue_by_category.values)
    
    ax.set_title('Total Revenue by Product Category')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Total Revenue')
    plt.xticks(rotation=45)

    fig.savefig(f'{output_dir}/revenue_by_category.png', dpi=150, bbox_inches='tight')
    plt.close(fig)


    # TODO: Chart 2 — Line chart: daily revenue trend
    daily_revenue = df.groupby('date')['revenue'].sum().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(daily_revenue.index, daily_revenue.values)

    ax.set_title('Daily Revenue Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Revenue')
    plt.xticks(rotation=45)

    fig.savefig(f'{output_dir}/daily_revenue_trend.png', dpi=150, bbox_inches='tight')
    plt.close(fig)


    # TODO: Chart 3 — Horizontal bar chart: avg order value by payment method
    avg_order_by_payment = df.groupby('payment_method')['revenue'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(avg_order_by_payment.index, avg_order_by_payment.values)

    ax.set_title('Average Order Value by Payment Method')
    ax.set_xlabel('Average Revenue')
    ax.set_ylabel('Payment Method')

    fig.savefig(f'{output_dir}/avg_order_by_payment.png', dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    """Run the full data pipeline end-to-end."""
    df= load_data(DATA_PATH)
    clean_D= clean_data(df)
    df=add_features(clean_D)
    summary = generate_summary(df)
    print("Summary Statistics:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    create_visualizations(df)
    print("Pipeline complete.") 


if __name__ == "__main__":
    main()
