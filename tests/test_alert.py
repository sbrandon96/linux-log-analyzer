import unittest
import os
from unittest.mock import patch
from dotenv import load_dotenv
from src.alert import send_alert

# Load environment variables
load_dotenv()

class TestAlert(unittest.TestCase):
    @patch.dict(os.environ, {
        'EMAIL_USERNAME': os.getenv('EMAIL_USERNAME', 'default_email'),
        'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD', 'default_password'),
        'EMAIL_HOST': os.getenv('EMAIL_HOST', 'smtp.mail.yahoo.com'),
        'EMAIL_PORT': os.getenv('EMAIL_PORT', '465'),
        'EMAIL_USE_SSL': os.getenv('EMAIL_USE_SSL', 'True')
    })
    @patch('src.alert.smtplib.SMTP_SSL')
    def test_send_alert(self, MockSMTP):
        # Set up the mock SMTP server
        mock_server = MockSMTP.return_value
        mock_server.sendmail.return_value = None  # Simulate successful sending

        # Call the function we want to test
        send_alert('Test Alert', 'This is a test message', 'test@example.com')

        # Check that the SMTP connection was established
        MockSMTP.assert_called_once_with('smtp.mail.yahoo.com', '465')

        # Check that the email was sent
        mock_server.sendmail.assert_called_once_with(
            os.getenv('EMAIL_USERNAME'),  # Dynamically pull sender email, 
            'test@example.com', 
            unittest.mock.ANY  # We use ANY because the message is dynamic
        )

        # Check that no exception was raised
        self.assertEqual(mock_server.sendmail.call_count, 1)

if __name__ == '__main__':
    unittest.main()
