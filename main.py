from datetime import datetime, timezone
import os
import logging
import requests
import sys

# Logging info
DEFAULT_LOG_LEVEL = os.environ.get("LOG_LEVEL") or logging.DEBUG
logging.getLogger().setLevel(DEFAULT_LOG_LEVEL)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

API_KEY = os.getenv("NSWWS_API_KEY")
HEADERS = {"X-Api-Key": API_KEY}

def get_nswws_feed():
    logging.info("Getting NSWWS feed...")
    response = requests.get("https://prd.nswws.api.metoffice.gov.uk/v1.0/objects/feed", headers=HEADERS)

    logging.debug(f"Response code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    return response.text

def get_datetime():
    now_utc = datetime.now(timezone.utc)
    formatted_datetime = now_utc.strftime("%Y-%m-%d_%H:%M:%S")
    return formatted_datetime

def find_previous_file(folder_path):
    previous_file = None

    with os.scandir(folder_path) as entries:
        for entry in entries:
            if not entry.name.endswith('.xml') or not entry.is_file():
                continue

            if previous_file is None or entry.name > previous_file:
                previous_file = entry.name

    logging.debug(f"Previous file: {previous_file}")
    return previous_file


def main():
    if not API_KEY:
        logging.critical("API Key not set")
        return 0

    feed_data = get_nswws_feed()
    formatted_datetime = get_datetime()

    # setup file path
    folder_path = "nswws_feed"
    filename = f"{formatted_datetime}.xml"
    file_path = os.path.join(folder_path, filename)

    # check if our file exists
    if os.path.isfile(file_path):
        logging.critical(f"File {filename} exists!")
        return 0
    
    # get previous file for comparison
    previous_filename = find_previous_file(folder_path)
    with open(f"{folder_path}/{previous_filename}", "r", encoding="utf-8") as previous_file:
        previous_file_contents = previous_file.read()

    if previous_file_contents == feed_data:
        logging.info(f"Previous file ({previous_filename}) is the same as the current data.")
        return 0

    # save our data
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(feed_data)
        logging.info(f"File {filename} was created.")

if __name__ == "__main__":
    main()
