import sys
import os
import unittest
from src.database import Database

# Get the parent directory and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from database import create_connection

conn = create_connection()
if conn:
    print("Database connection successful!")
    conn.close()
else:
    print("Database connection failed.")

class TestDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db = Database()
        cls.db.insert_mock_logs()
    
    def test_fetch_logs(self):
        db = Database()
        logs = db.fetch_logs(limit=5)
        db.close()
        
        self.assertIsInstance(logs, list)
        self.assertGreaterEqual(len(logs), 0)
        
    def test_fetch_logs_pretty(self):
        logs = self.db.fetch_logs_pretty(limit=5)
        print("\f fetch_logs_pretty:", logs)
        self.assertIsInstance(logs, list)
        self.assertGreater(len(logs), 0)
        self.assertIsInstance(logs[0], dict)
        
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        
if __name__ == "__main__":
    unittest.main()