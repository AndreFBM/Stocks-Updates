import pandas as pd
import os
from datetime import datetime
import urllib.request
from sqlalchemy import create_engine

# Path to the Excel file on the network
file_path = r"insertext"

# Read the specified sheet into a pandas DataFrame
df = pd.read_excel(file_path, sheet_name='Stock Local', engine='openpyxl')

# Get the last modified time of the file
last_modified_time = os.path.getmtime(file_path)
last_modified_date = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S.%f')
last_modified_date = last_modified_date[:-3]
df['ModifiedDate'] = last_modified_date

print(df)

quoted = urllib.parse.quote_plus(
    "DRIVER={SQL Server Native Client 11.0};SERVER='';DATABASE='';UID='';PWD='';")
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted}')

# Insert DataFrame into SQL Server as a table
table_name = "RPA_StockLocal_CashDisplay"
df.to_sql(table_name, schema='dbo', con=engine, if_exists='replace', index=False)
engine.dispose()

print(f"DataFrame inserted into '{table_name}' table in SQL Server.")
