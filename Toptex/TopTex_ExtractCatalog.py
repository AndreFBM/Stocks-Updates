import requests
import json
import pandas as pd

# Authentication details
AUTH_URL = "https://api.toptex.io/v3/authenticate"
API_KEY = "your_api_key"
AUTH_DATA = {
    "username": "your_username",
    "password": "your_password"
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
BASE_URL = "https://api.toptex.io/v3/products/all?usage_right=b2b_uniquement&page_number="
HEADERS["x-toptex-authorization"] = token

all_items = []
page_number = 1

while True:
    response = requests.get(BASE_URL + str(page_number), headers=HEADERS)
    page_data = response.json()

    # Check if page_data is a list and if it's empty, or if it's a dict without items.
    if isinstance(page_data, list) and not page_data or "items" not in page_data:
        break

    # If page_data is a dict and has an "items" key, extend the all_items list.
    if "items" in page_data:
        all_items.extend(page_data["items"])
        print(f"Retrieved data for page: {page_number}")
    page_number += 1

# Save the combined results to a JSON file in the specific folder
json_file_path = "path_to_save_json_file\\all_catalog.json"
with open(json_file_path, 'w') as f:
    json.dump({"items": all_items}, f)

# Convert the list of items to a pandas DataFrame
df = pd.DataFrame(all_items)

# Save the DataFrame to an Excel file
xlsx_file_path = json_file_path.replace('.json', '.xlsx')  # Assuming you want to save it in the same location
df.to_excel(xlsx_file_path, index=False)
