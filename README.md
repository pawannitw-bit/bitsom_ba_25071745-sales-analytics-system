# bitsom_ba_25071745-sales-analytics-system
# Sales Analytics System

The Sales Analytics System is a Python-based application developed to demonstrate end-to-end data handling, analytics, and reporting capabilities on structured sales data. The project focuses on data cleaning, validation, analytical processing, external API integration, and automated report generation to support business decision-making.

The system processes raw sales data, ensures data quality through predefined validation rules, performs multiple levels of analytical computation, enriches records using external product information, and generates a consolidated analytical report.


## Objectives

The key objectives of this assignment are:

To clean and validate raw transactional data using business rules

To perform descriptive and analytical computations on sales data

To integrate external API data for enrichment

To generate structured and interpretable analytical reports

To demonstrate modular and maintainable Python code design

### Prerequisites

- Python 3.7+
- pip

### Installation

1. **Navigate to project directory**

   ```bash
   cd sales-analytics-system
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**

   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python main.py
```

The application will process sales data, validate transactions, analyze trends, fetch product data from API, enrich transactions, and generate a comprehensive report.

### Interactive Filtering

When prompted, choose to filter data by region and amount range or proceed without filtering.

## Output Files

- `output/sales_report.txt` - Comprehensive analytics report
- `data/enriched_sales_data.txt` - Enriched transaction data
- `output/sales_data.csv` - Cleaned data in CSV format

## Troubleshooting

**ModuleNotFoundError**: Run `pip install -r requirements.txt`

**FileNotFoundError**: Ensure `data/sales_data.txt` exists in the correct location
FileNotFoundError: Ensure data/sales_data.txt exists in the correct location
