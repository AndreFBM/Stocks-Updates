# README

## Product Info Sync Script

This script aims to synchronize product information from the Garcia de Pou API to an SQL Server table.

### Features:
1. Establishes a connection to an SQL Server and fetches specific product references.
2. Makes API calls to the Garcia de Pou API to fetch product information using the retrieved product references.
3. Converts the fetched product information into a DataFrame and makes necessary column name adjustments.
4. Updates tables in SQL Server with the newly fetched product data.
5. Executes a merge operation to synchronize the fetched data.

### Pre-requisites:
- Python (with modules: pyodbc, pandas, requests, urllib, sqlalchemy)

### Usage:
Run the script using Python:
```
python <script_name>.py
```

### Step-by-step Breakdown:

1. **Connect to SQL Server and Retrieve Product References**:
    - Uses `pyodbc` to establish a connection with the specified SQL Server.
    - Executes a SQL query to fetch distinct product references.

2. **Make API Calls to Garcia de Pou**:
    - Utilizes the `requests` library to make POST requests to Garcia de Pou's API.
    - Retrieves product information in batches to ensure efficient data retrieval.

3. **Create DataFrame**:
    - Converts the fetched API data into a pandas DataFrame.
    - Adds a timestamp indicating the last update date.
    - Renames specific columns for consistency.

4. **Update Tables in SQL Server**:
    - Utilizes `sqlalchemy` to establish a connection and create an engine for SQL operations.
    - Replaces the existing data with the newly fetched product information.

5. **Execute the MERGE**:
    - Executes a SQL MERGE statement to synchronize the product data.

### Security Note:
Make sure to handle the tokens and passwords securely. Avoid exposing sensitive credentials in your script. Consider using environment variables or secure credential managers.

### Feedback & Issues:
For any feedback or issues related to this script, please contact the repository maintainer or raise an issue in the respective repository.
