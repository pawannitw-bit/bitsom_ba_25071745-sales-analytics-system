def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """

    try:
        with open(filename, 'r', encoding='cp1252') as file:
            lines = file.readlines()
            final_line = []
            for line in lines:
               if line.strip() == '':
                   continue
               final_line.append(line)
            return final_line[1:]
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []
    

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]

    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """

    transactions = []
    for line in raw_lines:
        parts = line.strip().split('|')
        if len(parts) != 8:
            continue

        transaction_id = parts[0]
        date = parts[1]
        product_id = parts[2]
        product_name = parts[3].replace(',', ' ')
        customer_id = parts[6]
        region = parts[7]
        try:
            quantity = int(parts[4].replace(',', ''))
            unit_price = float(parts[5].replace(',', ''))
        except ValueError:
            continue

        transaction = {
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        }
        transactions.append(transaction)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    valid_transactions = []
    invalid_count = 0
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }

    invalid_count, valid_transactions = get_valid_transaction(transactions=transactions)

    filter_summary['invalid'] = invalid_count

    if region:
        before_filtering = len(valid_transactions)
        valid_transactions = get_trnsaction_by_region(region, valid_transactions)
        filter_summary['filtered_by_region'] = before_filtering - len(valid_transactions)
    

    if min_amount is not None or max_amount is not None:
        valid_transactions = get_transaction_by_amout(min_amount, max_amount, valid_transactions, filter_summary)

    filter_summary['final_count'] = len(valid_transactions)

    return valid_transactions, invalid_count, filter_summary



def get_trnsaction_by_region(region, valid_transactions):
    region_transaction = []
    for valid_transaction in valid_transactions:
        if valid_transaction['Region'] == region:
            region_transaction.append(valid_transaction)
    return region_transaction


def get_valid_transaction(transactions):
    valid_transactions = []
    invalid_count = 0
    for transaction in transactions:
        try:
            if (transaction['Quantity'] <= 0 or
                transaction['UnitPrice'] <= 0 or
                not transaction['ProductID'].startswith('P') or
                not transaction['TransactionID'].startswith('T') or
                not transaction['CustomerID'].startswith('C')):
                invalid_count += 1
                continue
        except KeyError:
            invalid_count += 1
            continue
        valid_transactions.append(transaction)
    return invalid_count, valid_transactions

def get_transaction_by_amout(min_amount, max_amount, valid_transactions, filter_summary):
    before_count = len(valid_transactions)
    filter_by_amount = []
    for transaction in valid_transactions:
        amount = transaction['Quantity'] * transaction['UnitPrice']
        if min_amount is not None and amount < min_amount:
            continue
        if max_amount is not None and amount > max_amount:
            continue
        filter_by_amount.append(transaction)

    valid_transactions = filter_by_amount
    filter_summary['filtered_by_amount'] = before_count - len(valid_transactions)
    return valid_transactions
