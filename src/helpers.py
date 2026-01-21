from datetime import datetime, timezone
import logging
import os
import requests

def get_datetime():
    now_utc = datetime.now(timezone.utc)
    formatted_datetime = now_utc.strftime("%Y-%m-%d_%H:%M:%S")
    return formatted_datetime

def find_previous_file(folder_path, file_format):
    previous_file = None

    with os.scandir(folder_path) as entries:
        for entry in entries:
            if not entry.name.endswith(f'.{file_format}') or not entry.is_file():
                continue

            if previous_file is None or entry.name > previous_file:
                previous_file = entry.name

    logging.debug(f"Previous file: {previous_file}")
    return previous_file

def get_nswws_page(headers: str, path: str):
    NSWWS_BASE_URL = "https://prd.nswws.api.metoffice.gov.uk/v1.0/objects/"
    response = requests.get(f"{NSWWS_BASE_URL}{path}", headers=headers)

    # https://prd.nswws.api.metoffice.gov.uk/v1.0/objects/feed"
    # https://prd.nswws.api.metoffice.gov.uk/v1.0/objects/issued/{uuid}

    logging.debug(f"Response code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    return response.text

def does_file_exist(file_path):
    if os.path.isfile(file_path):
        logging.critical("File %s exists!", file_path)
        return True
    
    logging.info("File %s does not exist", file_path)
    return False

def get_file_content(file, path):
    filepath = f"{path}/{file}"
    logging.debug("Attempting to open %s", filepath)
    with open(f"{filepath}", "r", encoding="utf-8") as file:
        contents = file.read()
        return contents
    
def save_to_file(contents, filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(contents)
        logging.info("File %s was created", filepath)