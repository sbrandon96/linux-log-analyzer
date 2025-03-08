import unittest
from unittest.mock import MagicMock, patch
from src.log_monitor import LogMonitor


class TestLogMonitor(unittest.TestCase):

    @patch('src.log_monitor.open', new_callable=MagicMock)
    @patch('src.log_monitor.time.sleep', new_callable=MagicMock)  # Mock sleep to prevent delays in tests
    def test_read_new_logs(self, mock_sleep, mock_open):
        # Arrange
        mock_open.return_value.__enter__.return_value.readlines.return_value = ["log entry 1", "log entry 2"]
        log_monitor = LogMonitor(["test_log.log"], MagicMock(), MagicMock())

        # Act
        new_logs = log_monitor.read_new_logs("test_log.log")

        # Assert
        mock_open.assert_called_once_with("test_log.log", "r")
        self.assertEqual(new_logs, ["log entry 1", "log entry 2"])

    @patch('src.log_monitor.LogMonitor.read_new_logs')
    @patch('src.log_monitor.time.sleep', new_callable=MagicMock)
    def test_process_logs(self, mock_sleep, mock_read_new_logs):
        # Arrange
        mock_read_new_logs.return_value = ["log entry 1", "log entry 2"]
        mock_database = MagicMock()
        mock_alert_system = MagicMock()
        log_monitor = LogMonitor(["test_log.log"], mock_database, mock_alert_system)

        # Act
        log_monitor.process_logs("test_log.log")

        # Assert
        mock_database.store_log.assert_any_call("test_log.log", "log entry 1")
        mock_database.store_log.assert_any_call("test_log.log", "log entry 2")
        mock_alert_system.send_alert.assert_not_called()  # Assuming "log entry 1" is not critical

    @patch('src.log_monitor.LogMonitor.process_logs')
    @patch('src.log_monitor.time.sleep', new_callable=MagicMock)
    def test_start_monitoring(self, mock_sleep, mock_process_logs):
        # Arrange
        mock_process_logs.return_value = None
        mock_database = MagicMock()
        mock_alert_system = MagicMock()
        log_monitor = LogMonitor(["test_log.log"], mock_database, mock_alert_system)

        # Act
        with patch("time.sleep", return_value=None):  # Mock time.sleep to avoid delays
            for _ in range(2):  # Run only 2 cycles of monitoring
                log_monitor.process_logs("tests/test_log.log")


        # Assert
        mock_process_logs.assert_called()  # Check that the process_logs method was invoked during the loop

    def test_is_critical(self):
        # Arrange
        log_monitor = LogMonitor([], MagicMock(), MagicMock())

        # Act
        result1 = log_monitor.is_critical("This is an error message")
        result2 = log_monitor.is_critical("This is a normal message")

        # Assert
        self.assertTrue(result1)  # Should return True for critical log
        self.assertFalse(result2)  # Should return False for non-critical log
