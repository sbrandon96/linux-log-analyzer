import sys
import os

# Get the parent directory and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from database import create_connection

conn = create_connection()
if conn:
    print("Database connection successful!")
    conn.close()
else:
    print("Database connection failed.")
