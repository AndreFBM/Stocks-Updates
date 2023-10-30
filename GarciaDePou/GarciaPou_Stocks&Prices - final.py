import pyodbc
import pandas as pd
import requests
from datetime import datetime
import urllib.request
from sqlalchemy import create_engine, text

# --- Step 1: Connect to SQL Server and retrieve product references ---

# Connection string
conn_str = "Driver={SQL Server Native Client 11.0};Server='';Database='';UID='';PWD='';"
conn = pyodbc.connect(conn_str)

# SQL query
sql = """SELECT DISTINCT Productreference 
         FROM DW_360Imprimir.op.Supplier_Stock 
         WHERE SupplierName = 'Garcia de Pou'"""

# Fetch product references into a list
df = pd.read_sql(sql, conn)
product_refs = df['Productreference'].tolist()

# --- Step 2: Make API Calls ---

TOKEN = "your token"
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}
API_ENDPOINT = "https://axwebsrv.garciadepou.com/AppGdpWebSvc/dropshippingapi/DSApiCall"


def fetch_product_info(references):
    body = {
        "method": "ws_get_stocks_prices",
        "params": {
            "custAccount": "CLI200846",
            "nif": "PT509980422",
            "items": references
        }
    }

    response = requests.post(API_ENDPOINT, headers=HEADERS, json=body)
    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 200:
            return data.get('result', {}).get('items', [])
    return []


all_items = []

# Fetching product info in batches
for i in range(0, len(product_refs), 500):
    batch = product_refs[i:i + 500]
    items = fetch_product_info(batch)
    all_items.extend(items)

# --- Step 3: Create DataFrame ---

final_df = pd.DataFrame(all_items)
final_df['LastUpdateDate'] = datetime.now()

column_renames = {
    'sku': 'productreference',
    'units': 'Stock',
    'type': 'Type',
    'cost': 'Cost'
}

final_df.rename(columns=column_renames, inplace=True)

# --- STEP 4: Update tables ---

quoted = urllib.parse.quote_plus(
    "DRIVER={SQL Server Native Client 11.0};SERVER='';DATABASE='';UID='';PWD='';")
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted}')

table_name = "GarciaDePou_custos_new"
final_df.to_sql(table_name, schema='dbo', con=engine, if_exists='replace', index=False)
engine.dispose()

print(f"DataFrame inserted into '{table_name}' table in SQL Server.")

# Execute the MERGE

query = """
BEGIN
MERGE INTO [DW_360imprimir].[op].[supplier_stock] AS Target
	  USING (
			SELECT  
			[productreference] 'ProductReference',
			'Garcia de Pou' SupplierName,
			Stock 'ProductStock',
			LastUpdateDate 'LastUpdateDate',
			'EU' Store
			FROM [wkb_op].[dbo].[GarciaDePou_custos_new]
			) AS Source
	  ON (
			Target.SupplierName = Source.SupplierName
			AND Target.ProductReference = Source.ProductReference
		 )
		WHEN MATCHED THEN
		UPDATE SET 
			Target.ProductStock = Source.ProductStock,
			Target.LastUpdateDate = Source.LastUpdateDate;
END
"""

try:
    with engine.connect() as connection:
        connection.execute(text(query))
        connection.commit()  # Explicitly commit the transaction

    print("Merge Completed")

except Exception as e:
    print("An error occurred during query execution:", str(e))
