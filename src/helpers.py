from datetime import datetime, timezone

def get_datetime():
    now_utc = datetime.now(timezone.utc)
    formatted_datetime = now_utc.strftime("%Y-%m-%d_%H:%M:%S")
    return formatted_datetime