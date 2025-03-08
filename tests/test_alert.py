import unittest
from src.alert import send_alert
from unittest.mock import patch
import os

class TestAlert(unittest.TestCase):
    @patch.dict(os.environ, {
        'EMAIL_USERNAME': '[Insert Email Here]@yahoo.com',
        'EMAIL_PASSWORD': '[Insert Password Here]',
        'EMAIL_HOST': 'smtp.mail.yahoo.com',
        'EMAIL_PORT': '465',
        'EMAIL_USE_SSL': 'True'
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
            'sbrandon96@yahoo.com', 
            'test@example.com', 
            unittest.mock.ANY  # We use ANY because the message is dynamic
        )

        # Check that no exception was raised
        self.assertEqual(mock_server.sendmail.call_count, 1)

if __name__ == '__main__':
    unittest.main()
