def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total_revenue = 0
    for transaction in transactions:
        try:
            quantity = transaction['Quantity']
            unit_price = transaction['UnitPrice']
            total_revenue += quantity * unit_price
        except KeyError:
            continue
    return total_revenue


def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }

    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """

    region_stats = {}
    total_sales = 0

    for transaction in transactions:
        try:
            region = transaction['Region']
            sales_amount = transaction['Quantity'] * transaction['UnitPrice']
        except KeyError:
            continue

        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0,
                'transaction_count': 0
            }

        total_sales += sales_amount
        region_stats[region]['total_sales'] += sales_amount
        region_stats[region]['transaction_count'] += 1

    for region, stats in region_stats.items():
        if total_sales > 0:
            stats['percentage'] = round((stats['total_sales'] / total_sales) * 100, 2)
        else:
            stats['percentage'] = 0.0

    sorted_region_stats = dict(sorted(region_stats.items(), key=lambda item: item[1]['total_sales'], reverse=True))

    return sorted_region_stats

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples

    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]

    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    product_stats = {}

    get_product_stats(transactions, product_stats)

    sorted_products = sorted(product_stats.items(), key=lambda item: item[1]['total_quantity'], reverse=True)

    top_n_products = []

    for product, stats in sorted_products[:n]:
        top_n_products.append((product, stats['total_quantity'], stats['total_revenue']))

    return top_n_products



def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics

    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }

    Requirements:
    - Calculate total amount spent per customer
    - Count number of purchases
    - Calculate average order value
    - List unique products bought
    - Sort by total_spent descending
    """

    customer_stats = {}

    for transaction in transactions:
        try:
            customer_id = transaction['CustomerID']
            product_name = transaction['ProductName']
            amount_spent = transaction['Quantity'] * transaction['UnitPrice']
        except KeyError:
            continue

        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_stats[customer_id]['total_spent'] += amount_spent
        customer_stats[customer_id]['purchase_count'] += 1
        customer_stats[customer_id]['products_bought'].add(product_name)

    for customer_id, stats in customer_stats.items():
        if stats['purchase_count'] > 0:
            stats['avg_order_value'] = round(stats['total_spent'] / stats['purchase_count'], 2)
        else:
            stats['avg_order_value'] = 0.0
        stats['products_bought'] = list(stats['products_bought'])

    sorted_customer_stats = dict(sorted(customer_stats.items(), key=lambda item: item[1]['total_spent'], reverse=True))

    return sorted_customer_stats


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date

    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }

    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """

    date_stats = {}

    for transaction in transactions:
        try:
            date = transaction['Date']
            customer_id = transaction['CustomerID']
            amount_spent = transaction['Quantity'] * transaction['UnitPrice']
        except KeyError:
            continue

        if date not in date_stats:
            date_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': []
            }

        date_stats[date]['revenue'] += amount_spent
        date_stats[date]['transaction_count'] += 1
        date_stats[date]['unique_customers'].append(customer_id)

    for date, stats in date_stats.items():
        stats['unique_customers'] = len(set(stats['unique_customers']))
        

    sorted_date_stats = dict(sorted(date_stats.items(), key=lambda item: item[0]))

    return sorted_date_stats

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)

    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """

    daily_stats = daily_sales_trend(transactions)
    peak_day = None
    max_revenue = 0.0
    transaction_count = 0

    for date, stats in daily_stats.items():
        if stats['revenue'] > max_revenue:
            max_revenue = stats['revenue']
            peak_day = date
            transaction_count = stats['transaction_count']

    return (peak_day, max_revenue, transaction_count)


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples

    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]

    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """

    product_stats = {}

    get_product_stats(transactions=transactions, product_stats=product_stats)

    low_performers = []

    for product, stats in product_stats.items():
        if stats['total_quantity'] < threshold:
            low_performers.append((product, stats['total_quantity'], stats['total_revenue']))

    low_performers.sort(key=lambda x: x[1])

    return low_performers


def get_product_stats(transactions, product_stats):
    for transaction in transactions:
        try:
            product_name = transaction['ProductName']
            quantity = transaction['Quantity']
            unit_price = transaction['UnitPrice']
        except KeyError:
            continue

        if product_name not in product_stats:
            product_stats[product_name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_stats[product_name]['total_quantity'] += quantity
        product_stats[product_name]['total_revenue'] += quantity * unit_price
