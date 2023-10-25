import os
import pandas as pd
from datetime import datetime
import urllib.request
from sqlalchemy import create_engine, text


path = os.environ.get('FILE_PATH')
server_address = os.environ.get('SERVER_ADDRESS')
database_name = os.environ.get('DATABASE_NAME')
user_id = os.environ.get('USER_ID')
password = os.environ.get('PASSWORD')

if os.path.exists(path):
    xlsx_files = [f for f in os.listdir(path) if f.endswith('.xlsx')]

    if xlsx_files:
        stock_file = next((f for f in xlsx_files if 'stock' in f.lower()), None)

        if stock_file:
            df = pd.read_excel(os.path.join(path, stock_file), dtype={0: str})

            rename_dict = {}
            for col in df.columns:
                if "referência" in col.lower():
                    rename_dict[col] = "Reference"
                elif "nome" in col.lower():
                    rename_dict[col] = "Name"

            df.rename(columns=rename_dict, inplace=True)

            timestamp = os.path.getmtime(os.path.join(path, stock_file))
            last_modified_date = datetime.fromtimestamp(timestamp)

            df["LastUpdateDate"] = last_modified_date
            df.drop_duplicates(inplace=True)

            quoted = urllib.parse.quote_plus(
                f"DRIVER={{SQL Server Native Client 11.0}};SERVER={server_address};DATABASE={database_name};UID={user_id};PWD={password};")
            engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted}')

            table_name = "RPA_Stocks_MPS"
            df.to_sql(table_name, schema='dbo', con=engine, if_exists='replace', index=False)
            engine.dispose()

            print(f"DataFrame inserted into '{table_name}' table in SQL Server.")

            # Execute the MERGE
            query = """
            """

            try:
                with engine.connect() as connection:
                    connection.execute(text(query))
                    connection.commit()

                print("SQL query executed.")

            except Exception as e:
                print("An error occurred during query execution:", str(e))

        else:
            print("No xlsx file with the word 'stock' in its name was found.")
    else:
        print("No xlsx files found in the path.")
else:
    print("The specified path does not exist.")
