import re

# Sample regex pattern for basic log format
LOG_PATTERN = r"(?P<timestamp>\S+ \S+) (?P<host>\S+) (?P<service>\S+) \[(?P<level>\S+)\] (?P<message>.*)"

def parse_log_line(line):
    """
    Parse a single line of log and extract relevant fields using regex.

    Args:
    - line (str): A line of log data

    Returns:
    - dict: Parsed log data as key-value pairs
    """
    match = re.match(LOG_PATTERN, line)
    if match:
        return match.groupdict()  # Return as dictionary with named groups
    else:
        return None  # Return None if the log doesn't match the expected pattern
