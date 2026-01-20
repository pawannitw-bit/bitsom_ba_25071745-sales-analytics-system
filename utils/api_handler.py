import requests
import pandas as pd

from utils.data_processor import calculate_total_revenue, customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products, region_wise_sales, top_selling_products
def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries

    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """

   

    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url)
        data = response.json()
        products = data.get('products', [])
        print(f"Successfully fetched {len(products)} products.")
        return products
    except requests.RequestException as e:
        print(f"Failed to fetch products: {e}")
        return []
    

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info

    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """

    product_mapping = {}
    for product in api_products:
        try:
            product_id = product['id']
            product_info = {
                'title': product['title'],
                'category': product['category'],
                'brand': product['brand'],
                'rating': product['rating']
            }
            product_mapping[product_id] = product_info
        except KeyError as e:
            print(f"Missing expected key in product data: {e}")
            continue
    return product_mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns: list of enriched transaction dictionaries

    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True  # True if enrichment successful, False otherwise
    }

    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match to False and other fields to None
    - Handle all errors gracefully

    File Output:
    - Save enriched data to 'data/enriched_sales_data.txt'
    - Use same pipe-delimited format
    - Include new columns in header
    """
    enriched_transactions = []
    for transaction in transactions:
        enriched_transaction = transaction.copy()
        product_id_str = transaction.get('ProductID', '')
        try:
            product_id = int(product_id_str.lstrip('P1'))
            if product_id in product_mapping:
                product_info = product_mapping[product_id]
                enriched_transaction['API_Category'] = product_info['category']
                enriched_transaction['API_Brand'] = product_info['brand']
                enriched_transaction['API_Rating'] = product_info['rating']
                enriched_transaction['API_Match'] = True
            else:
                enriched_transaction['API_Category'] = None
                enriched_transaction['API_Brand'] = None
                enriched_transaction['API_Rating'] = None
                enriched_transaction['API_Match'] = False
        except (ValueError, KeyError) as e:
            print(f"Error processing ProductID '{product_id_str}': {e}")
            enriched_transaction['API_Category'] = None
            enriched_transaction['API_Brand'] = None
            enriched_transaction['API_Rating'] = None
            enriched_transaction['API_Match'] = False
        
        enriched_transactions.append(enriched_transaction)

    save_enriched_data(enriched_transactions, 'data/enriched_sales_data.txt')
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """

    output_file = filename
    with open(output_file, 'w', encoding='utf-8') as f:
        headers = list(enriched_transactions[0].keys())
        f.write('|'.join(headers) + '\n')
        for transaction in enriched_transactions:
            row = [str(transaction.get(header, '')) for header in headers]
            f.write('|'.join(row) + '\n')
    print(f"Enriched data saved to {output_file}")


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report

    Report Must Include (in this order):

    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed

    2. OVERALL SUMMARY
       - Total Revenue (formatted with commas)
       - Total Transactions
       - Average Order Value
       - Date Range of data

    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total Sales Amount
         * Percentage of Total
         * Transaction Count
       - Sorted by sales amount descending

    4. TOP 5 PRODUCTS
       - Table with columns: Rank, Product Name, Quantity Sold, Revenue

    5. TOP 5 CUSTOMERS
       - Table with columns: Rank, Customer ID, Total Spent, Order Count

    6. DAILY SALES TREND
       - Table showing: Date, Revenue, Transactions, Unique Customers

    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region

    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched

    Expected Output Format (sample):
    ============================================
           SALES ANALYTICS REPORT
         Generated: 2024-12-18 14:30:22
         Records Processed: 95
    ============================================

    OVERALL SUMMARY
    --------------------------------------------
    Total Revenue:        ₹15,45,000.00
    Total Transactions:   95
    Average Order Value:  ₹16,263.16
    Date Range:           2024-12-01 to 2024-12-31

    REGION-WISE PERFORMANCE
    --------------------------------------------
    Region    Sales         % of Total  Transactions
    North     ₹4,50,000     29.13%      25
    South     ₹3,80,000     24.60%      22
    ...

    (continue with all sections...)
    """
    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    average_order_value = total_revenue / total_transactions
    date_range = f"{min(t['Date'] for t in transactions)} to {max(t['Date'] for t in transactions)}"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("============================================\n")
        f.write("      SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {pd.Timestamp.now()}\n")
        f.write(f"     Records Processed: {total_transactions}\n")
        f.write("============================================\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("--------------------------------------------\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{average_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION-WISE PERFORMANCE.
        region_sales = region_wise_sales(transactions)
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Region':<20} {'Sales':<20} {'% of Total':<15} {'Transactions':<15}\n")
        for region, sales in region_sales.items():
            region_name = region if region else 'No region'
            sales_amount = f"₹{sales['total_sales']:,.2f}"
            percentage = f"{sales['percentage']:.2f}%"
            transaction_count = sales.get('transaction_count', 0)
            f.write(f"{region_name:<20} {sales_amount:<20} {percentage:<15} {transaction_count:<15}\n")
        f.write("\n")

        # TOP 5 PRODUCTS
        top_products = top_selling_products(transactions, 5)
        f.write("TOP 5 PRODUCTS\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Rank':<5} {'Product Name':<30} {'Quantity Sold':<15} {'Revenue':<15}\n")
        for rank,(productname, quantity, total_revenue) in enumerate(top_products, start=1):
            f.write(f"{rank:<5} {productname:<30} {quantity:<15} ₹{total_revenue:,.2f}\n")
        f.write("\n")

        # TOP 5 CUSTOMERS
        customer_data = customer_analysis(transactions)
        top_customers = sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
        f.write("TOP 5 CUSTOMERS\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Rank':<5} {'Customer ID':<20} {'Total Spent':<20} {'Order Count':<15}\n")
        for rank, (customer_id, value) in enumerate(top_customers, start=1):
            f.write(f"{rank:<5} {customer_id:<20} ₹{value['total_spent']:<20,.2f} {value['purchase_count']:<15}\n")
        f.write("\n")


        # DAILY SALES TREND
        daily_trend = daily_sales_trend(transactions)
        f.write("DAILY SALES TREND\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<20}\n")
        for date, data in daily_trend.items():
            f.write(f"{date:<15} ₹{data['revenue']:<20,.2f} {data['transaction_count']:<15} {data['unique_customers']:<20}\n")
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS

        peak_day, max_revenue, _ = find_peak_sales_day(transactions)
        low_performers = low_performing_products(transactions, threshold=14)
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("--------------------------------------------\n")
        f.write(f"Best Selling Day: {peak_day} with Revenue ₹{max_revenue:,.2f}\n")
        if low_performers:
            f.write("Low Performing Products (less than 14 days sold):\n")
            for product in low_performers:
                f.write(f" - {product}\n")
        else:
            f.write("No low performing products.\n")
        f.write("\n")

        # API ENRICHMENT SUMMARY
        total_enriched = len(enriched_transactions)
        successful_enriched_products = []
        failed_enriched_products = 0
        for enriched_transaction in enriched_transactions:
            if enriched_transaction.get('API_Match') == False:
                failed_enriched_products += 1
            else: 
                successful_enriched_products.append(enriched_transaction.get('ProductID'))
               
        success_rate = (len(successful_enriched_products) / total_enriched) * 100 if total_enriched > 0 else 0
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("--------------------------------------------\n")
        f.write(f"Total Products Enriched: {total_enriched}\n")
        f.write(f"Successful Enrichment Rate: {success_rate:.2f}%\n")
        f.write("Products that couldn't be enriched:\n")
        for product in successful_enriched_products:
            f.write(f" - {product}\n")

    print(f"Sales report generated and saved to {output_file}")

