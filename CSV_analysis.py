import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_sample_data():
    """Create sample sales data if CSV doesn't exist"""
    print("Creating sample sales data...")
    
    # Sample data
    np.random.seed(42)
    data = {
        'Date': pd.date_range('2024-01-01', periods=500, freq='D'),
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones'], 500),
        'Category': np.random.choice(['Electronics', 'Accessories'], 500),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 500),
        'Salesperson': np.random.choice(['Alice', 'Bob', 'Carol', 'David'], 500),
        'Units_Sold': np.random.randint(1, 20, 500),
        'Price_Per_Unit': np.random.randint(50, 500, 500)
    }
    
    df = pd.DataFrame(data)
    df['Total_Sales'] = df['Units_Sold'] * df['Price_Per_Unit']
    df['Month'] = df['Date'].dt.month_name()
    
    # Save to CSV
    df.to_csv('sales_data.csv', index=False)
    print("Sample data saved as 'sales_data.csv'")
    return df

def load_data():
    """Load sales data from CSV"""
    try:
        df = pd.read_csv('sales_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        print(f"Data loaded: {len(df)} records")
        return df
    except FileNotFoundError:
        print("CSV file not found, creating sample data...")
        return create_sample_data()

def basic_analysis(df):
    """Basic data exploration"""
    print("\n=== BASIC DATA ANALYSIS ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nBasic statistics:")
    print(df[['Units_Sold', 'Price_Per_Unit', 'Total_Sales']].describe())

def sales_by_category(df):
    """Analyze sales by product category"""
    print("\n=== SALES BY CATEGORY ===")
    
    # Group by category and calculate totals
    category_sales = df.groupby('Category').agg({
        'Total_Sales': 'sum',
        'Units_Sold': 'sum'
    }).round(2)
    
    print("Sales by Category:")
    print(category_sales)
    
    # Create chart
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    category_sales['Total_Sales'].plot(kind='bar', color='skyblue')
    plt.title('Total Sales by Category')
    plt.ylabel('Sales ($)')
    plt.xticks(rotation=45)
    
    plt.subplot(1, 2, 2)
    category_sales['Units_Sold'].plot(kind='bar', color='lightgreen')
    plt.title('Units Sold by Category')
    plt.ylabel('Units')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return category_sales

def sales_by_region(df):
    """Analyze sales by region"""
    print("\n=== SALES BY REGION ===")
    
    # Group by region
    region_sales = df.groupby('Region').agg({
        'Total_Sales': 'sum',
        'Units_Sold': 'sum'
    }).round(2)
    
    print("Sales by Region:")
    print(region_sales)
    
    # Create chart
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    region_sales['Total_Sales'].plot(kind='bar', color='orange')
    plt.title('Total Sales by Region')
    plt.ylabel('Sales ($)')
    plt.xticks(rotation=45)
    
    plt.subplot(1, 2, 2)
    region_sales['Total_Sales'].plot(kind='pie', autopct='%1.1f%%')
    plt.title('Sales Distribution by Region')
    
    plt.tight_layout()
    plt.show()
    
    return region_sales

def monthly_trends(df):
    """Analyze monthly sales trends"""
    print("\n=== MONTHLY TRENDS ===")
    
    # Group by month
    monthly_sales = df.groupby('Month')['Total_Sales'].sum().round(2)
    
    print("Monthly Sales:")
    print(monthly_sales)
    
    # Create trend chart
    plt.figure(figsize=(12, 6))
    monthly_sales.plot(kind='line', marker='o', linewidth=2, markersize=8)
    plt.title('Monthly Sales Trend')
    plt.ylabel('Total Sales ($)')
    plt.xlabel('Month')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()
    
    return monthly_sales

def top_performers(df):
    """Analyze top performing salespersons"""
    print("\n=== TOP PERFORMERS ===")
    
    # Group by salesperson
    salesperson_sales = df.groupby('Salesperson').agg({
        'Total_Sales': 'sum',
        'Units_Sold': 'sum'
    }).round(2)
    
    # Sort by total sales
    salesperson_sales = salesperson_sales.sort_values('Total_Sales', ascending=False)
    
    print("Sales by Salesperson:")
    print(salesperson_sales)
    
    # Create chart
    plt.figure(figsize=(10, 6))
    salesperson_sales['Total_Sales'].plot(kind='bar', color='gold')
    plt.title('Total Sales by Salesperson')
    plt.ylabel('Sales ($)')
    plt.xticks(rotation=45)
    plt.show()
    
    return salesperson_sales

def summary_report(df):
    """Generate summary report"""
    print("\n=== SUMMARY REPORT ===")
    
    total_sales = df['Total_Sales'].sum()
    total_units = df['Units_Sold'].sum()
    avg_sale = df['Total_Sales'].mean()
    
    print(f"Total Revenue: ${total_sales:,.2f}")
    print(f"Total Units Sold: {total_units:,}")
    print(f"Average Sale: ${avg_sale:.2f}")
    print(f"Number of Transactions: {len(df)}")
    
    # Best performers
    best_category = df.groupby('Category')['Total_Sales'].sum().idxmax()
    best_region = df.groupby('Region')['Total_Sales'].sum().idxmax()
    best_salesperson = df.groupby('Salesperson')['Total_Sales'].sum().idxmax()
    
    print(f"\nTop Category: {best_category}")
    print(f"Top Region: {best_region}")
    print(f"Top Salesperson: {best_salesperson}")

def main():
    """Main function to run all analyses"""
    print("SALES DATA ANALYSIS")
    print("=" * 30)
    
    # Load data
    df = load_data()
    
    # Run analyses
    basic_analysis(df)
    sales_by_category(df)
    sales_by_region(df)
    monthly_trends(df)
    top_performers(df)
    summary_report(df)
    
    print("\n Analysis completed!")

# Run the analysis
if __name__ == "__main__":
    main()

# Additional simple functions you can use:

def analyze_product(df, product_name):
    """Analyze specific product performance"""
    product_data = df[df['Product'] == product_name]
    if len(product_data) > 0:
        total_sales = product_data['Total_Sales'].sum()
        units_sold = product_data['Units_Sold'].sum()
        print(f"\n{product_name} Performance:")
        print(f"Total Sales: ${total_sales:,.2f}")
        print(f"Units Sold: {units_sold}")
    else:
        print(f"No data found for {product_name}")

def top_products(df, n=5):
    """Show top N products by sales"""
    top_products = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False).head(n)
    print(f"\nTop {n} Products by Sales:")
    for i, (product, sales) in enumerate(top_products.items(), 1):
        print(f"{i}. {product}: ${sales:,.2f}")

