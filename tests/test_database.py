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
    def test_fetch_logs(self):
        db = Database()
        logs = db.fetch_logs(limit=5)
        db.close()
        
        self.assertIsInstance(logs, list)
        self.assertGreaterEqual(len(logs), 0)
        
if __name__ == "__main__":
    unittest.main()