import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import shutil

def start_download_process(download_dir, shared_folder_link):
    options = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing_for_trusted_sources_enabled': False,
        'safebrowsing.enabled': False
    }
    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(options=options)

    # Go to shared folder link
    browser.get(shared_folder_link)
    time.sleep(5)

    # Click the 'Transferir tudo' button
    download_all_button = browser.find_element(By.CSS_SELECTOR, "div.h-sb-Ic.h-R-d.a-c-d.a-r-d.a-R-d.a-s-Ba-d-Mr-Be-nAm6yf") # might need updates
    download_all_button.click()

    # Wait until the download is complete
    time.sleep(60)

    while any(fname.endswith('.crdownload') for fname in os.listdir(download_dir)):
        time.sleep(2)

    browser.quit()

    # Delete everything in the download_dir except the ZIP file
    for file_name_to_delete in os.listdir(download_dir):
        full_path = os.path.join(download_dir, file_name_to_delete)

        if os.path.isfile(full_path) and not file_name_to_delete.endswith('.zip'):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)

    # Unzip the downloaded file
    for file_name in os.listdir(download_dir):
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(download_dir, file_name), 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            # Delete the ZIP file
            os.remove(os.path.join(download_dir, file_name))

if __name__ == "__main__":
    download_dir = input("Enter download directory path: ")
    shared_folder_link = input("Enter shared folder link: ")
    start_download_process(download_dir, shared_folder_link)
