from datetime import datetime

def convert_timestamp(timestamp_str):
    """
    Convert a string timestamp into a Python datetime object.

    Args:
    - timestamp_str (str): A timestamp string, e.g., '2025-03-05 12:30:45'

    Returns:
    - datetime: Python datetime object
    """
    try:
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None  # Return None if the format is incorrect

# You could add other helper functions here, like date formatting, regex helpers, etc.
