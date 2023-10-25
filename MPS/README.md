## Script DownloadFile:

**Purpose**: To automate the process of downloading files from a specified Google Drive link using a web browser.

**Steps:**

Set a specified directory as the default download location for the web browser.
Open a web browser (specifically Chrome) and navigate to a given Google Drive link.
Click on a button (assumed to be the 'Transferir tudo' button) to initiate the downloading of files.
Wait for the download to complete by monitoring the download directory for any files with the .crdownload extension.
Close the browser once the download is complete.
Clean up the download directory by removing all files that aren't ZIP files and deleting any sub-directories.
Unzip any ZIP files found in the download directory and remove the original ZIP files afterward.

## Script UpdateStocks:

**Purpose:** To process and upload Excel files containing stock data from a specified directory to an SQL Server.

**Steps:**

Check if a specified directory path exists.
If it does, list all the Excel (.xlsx) files present.
From the list, find a file with 'stock' in its name.
Read the selected Excel file into a DataFrame and rename certain columns.
Add a column for the file's last modified date.
Remove any duplicate rows from the DataFrame.
Connect to an SQL Server using specified connection details.
Upload the processed DataFrame to a table (RPA_Stocks_MPS) in the SQL Server, replacing the table if it already exists.
Execute a SQL MERGE query that updates a target table in the database using the data from the uploaded table.
Provide feedback on whether the operations were successful or if any errors occurred during the process.

In essence, the first script automates downloading and unzipping files from a Google Drive link, while the second script processes stock data from Excel files and uploads it to an SQL Server database.
