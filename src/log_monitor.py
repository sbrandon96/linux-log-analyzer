import time  # For sleep intervals in monitoring loop
import os  # For file handling
import logging  # For logging status messages


class LogMonitor:
    def __init__(self, log_files, database, alert_system, interval=2):
        """
        Initializes the LogMonitor.

        :param log_files: List of log file paths to monitor.
        :param database: Database instance to store logs.
        :param alert_system: AlertSystem instance to send notifications.
        :param interval: Time in seconds between file checks.
        """
        self.log_files = log_files
        self.database = database
        self.alert_system = alert_system
        self.interval = interval
        self.log_positions = {log_file: 0 for log_file in log_files}  # Keeps track of where we last read in each file


    def read_new_logs(self, log_file):
        """Reads new log entries from the specified file."""
        if not os.path.exists(log_file):
            logging.warning(f"Log file {log_file} not found.")
            return []
        
        new_lines = []
        with open(log_file, "r") as file:
            file.seek(self.log_positions[log_file])  # Move to last read position
            new_lines = file.readlines()  # Read any new lines
            self.log_positions[log_file] = file.tell()  # Update last read position
        
        return new_lines


    def process_logs(self, log_file):
        """Processes new log entries and stores them in the database."""
        new_logs = self.read_new_logs(log_file)
        
        for log_entry in new_logs:
            logging.info(f"New log detected: {log_entry.strip()}")
            self.database.store_log(log_file, log_entry)  # Store log in database
            
            if self.is_critical(log_entry):
                self.alert_system.send_alert(log_file, log_entry)  # Trigger alert


    def is_critical(self, log_entry):
        """Checks if a log entry is critical."""
        critical_keywords = ["error", "failed", "unauthorized", "critical"]  # Define critical terms
        return any(keyword in log_entry.lower() for keyword in critical_keywords)


    def start(self):
        """Starts monitoring the log files in real-time."""
        logging.info("Log monitoring started.")
        
        try:
            while True:
                for log_file in self.log_files:
                    self.process_logs(log_file)
                time.sleep(self.interval)  # Wait before checking again
        except KeyboardInterrupt:
            logging.info("Log monitoring stopped.")
