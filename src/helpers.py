from datetime import datetime, timezone
import logging
import os

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
