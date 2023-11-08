```markdown
# TopTex API Data Retrieval and Processing

This repository contains two Python scripts designed for interacting with the TopTex API. The scripts authenticate with the API, retrieve product inventory data, and perform data transformation and storage operations.

## Scripts Description

### Script 1: Data Retrieval and Database Insertion

`Toptex_Stocks.py` connects to the TopTex API, retrieves the full inventory of products, processes the data, and inserts it into a SQL database. It also executes a SQL MERGE query to update an existing data warehouse.

#### Features

- Authentication with the TopTex API
- Data retrieval with pagination
- JSON data storage
- Data transformation to a structured format
- Insertion of data into a SQL Server database
- Execution of a SQL MERGE query

### Script 2: Data Retrieval and Conversion to Excel

`Toptex_ExtractCatalog.py` performs a similar data retrieval process but focuses on converting the retrieved JSON data directly into an Excel file.

#### Features

- Authentication with the TopTex API
- Data retrieval with pagination
- JSON data storage
- Conversion of JSON data to an Excel file

## Setup

### Requirements

- Python 3.x
- Libraries: `requests`, `json`, `pandas`, `sqlalchemy`, `datetime`, `urllib.parse`
- SQL Server or compatible SQL database

### Installation

Install the required Python libraries using pip:

```sh
pip install requests pandas sqlalchemy pyodbc openpyxl
```

### Configuration

Before running the scripts, you need to configure the following:

- Replace `<your_api_key>`, `<your_username>`, and `<your_password>` with your actual API key, username, and password for the TopTex API.
- Set up the correct SQL Server connection details in the connection string within the script.
- Specify the file paths for JSON and Excel file outputs.
- Customize the SQL queries as per your database schema.

## Usage

To run the scripts, execute the following command in your terminal:

```sh
python Toptex_Stocks.py
python Toptex_ExtractCatalog.py
```

## Important Notes

- Keep your API credentials confidential and secure.
- Ensure that the database connection string is stored securely and not exposed in the version control.
- The scripts may need to be adapted if the TopTex API changes its interface or data format.

```

Make sure to replace placeholder text like `<your_api_key>`, `<your_username>`, `<your_password>`, `<your_contact_information>`, and `[Insert License Here]` with the appropriate information. Additionally, the file paths and database schema details should be correctly configured as per the environment where the scripts will be run.
