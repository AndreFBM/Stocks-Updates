import requests
import json
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import urllib.parse

# Authentication details
AUTH_URL = "https://api.toptex.io/v3/authenticate"
API_KEY = "<your_api_key>"
AUTH_DATA = {
    "username": "<your_username>",
    "password": "<your_password>"
}
HEADERS = {
    "x-api-key": API_KEY
}

# Authenticate
response = requests.post(AUTH_URL, headers=HEADERS, json=AUTH_DATA)
response_data = response.json()

if response.status_code == 200:
    token = response_data["token"]
    print("Authentication successful. Retrieved token.")
else:
    print(f"Error: {response_data.get('message', 'Failed to authenticate')}")
    exit(1)

# Get products inventory
BASE_URL = "https://api.toptex.io/v3/products/inventory?modified_since=all&page_size=10000&page_number="
HEADERS["x-toptex-authorization"] = token

all_items = []
page_number = 1

while True:
    response = requests.get(BASE_URL + str(page_number), headers=HEADERS)
    page_data = response.json()

    if not page_data["items"]:
        break

    all_items.extend(page_data["items"])
    print(f"Retrieved data for page: {page_number}")
    page_number += 1

# Save the combined results to a JSON file in the specific folder
file_path = "<network_path_to_your_json_file>"
with open(file_path, 'w') as f:
    json.dump({"items": all_items}, f)

# Convert to DataFrame
processed_data = []
for item in all_items:
    row = {
        "sku": item["sku"],
        "catalogReference": item["catalogReference"],
        "designation": item["designation"],
        "colorCode": item["colorCode"],
        "sizeCode": item["sizeCode"],
        "color": item["color"],
        "size": item["size"]
    }

    stock_value = None
    for warehouse in item["warehouses"]:
        if warehouse["id"] == "<warehouse_id>":
            stock_value = int(warehouse["stock"])
            break
    row["stock"] = stock_value if stock_value is not None else 0
    processed_data.append(row)

df = pd.DataFrame(processed_data)
df["LastUpdateDate"] = datetime.now()

# SQL Server connection details
connection_string = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=<your_server_address>;"
    "DATABASE=<your_database_name>;"
    "UID=<your_username>;"
    "PWD=<your_password>;"
)
quoted_conn_str = urllib.parse.quote_plus(connection_string)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')

table_name = "RPA_Stocks_Toptex"
df.to_sql(table_name, schema='dbo', con=engine, if_exists='replace', index=False)
engine.dispose()

print(f"DataFrame inserted into '{table_name}' table in SQL Server.")

# Execute the SQL query
query = """
BEGIN

    MERGE INTO [DW_360imprimir].[op].[supplier_stock] AS Target
    USING (
        SELECT  sku 'ProductReference',
        color 'ProductColor',
        size 'ProductSize',
        'TopTex' SupplierName,
        Stock 'ProductStock',
        LastUpdateDate 'LastUpdateDate',
        'EU' Store
        FROM [wkb_op].[dbo].[RPA_Stocks_Toptex]
        ) AS Source
    ON  (
        Target.SupplierName = Source.SupplierName
        AND Target.ProductReference = Source.ProductReference
        )
    WHEN MATCHED THEN
    UPDATE SET 
        Target.ProductColor = Source.ProductColor,
        Target.ProductSize = Source.ProductSize,
        Target.ProductStock = Source.ProductStock,
        Target.LastUpdateDate = Source.LastUpdateDate
    WHEN NOT MATCHED THEN           
        INSERT ([SupplierName] ,[ProductReference], [ProductColor], [ProductSize] ,[ProductStock],[LastUpdateDate],[Store])
        VALUES (Source.SupplierName, Source.ProductReference,Source.ProductColor,Source.ProductSize,Source.ProductStock,Source.LastUpdateDate,Source.Store);
END
"""
print("Executing SQL query:")

try:
    with engine.connect() as connection:
        connection.execute(text(query))
        connection.commit()  # Explicitly commit the transaction

    print("SQL query executed.")

except Exception as e:
    print("An error occurred during query execution:", str(e))
