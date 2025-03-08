import os
from dotenv import load_dotenv
from src.alert import send_alert

# Load environment variables
load_dotenv()

#Manually test the email function
send_alert('Test Alert', 'This is a test message', os.getenv('TEST_EMAIL'))