import yaml  # For reading configuration files
import logging  # For logging errors and status messages
from src.log_monitor import LogMonitor  # Our log monitoring class
from src.database import Database  # Handles SQL database interactions
from src.alert import AlertSystem  # Sends alerts on critical events


def load_config(config_path="config/config.yaml"):
    """Loads configuration settings from a YAML file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config()
    
    # Initialize logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    # Create instances of core components
    db = Database(config["database"])
    alert_system = AlertSystem(config["email"])
    log_monitor = LogMonitor(config["log_files"], db, alert_system)

    logging.info("Linux Log Analyzer started.")
    
    # Start monitoring logs
    log_monitor.start()
