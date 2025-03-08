import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables (database credentials from .env file)
load_dotenv()

def create_connection():
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
            )
            return conn
        except Exception as e:
            print("Database connection error:", e)
            return None

class Database:
    def __init__(self):
        """Initialize the database connection using credentials from environment variables."""
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.cursor = self.conn.cursor()
            print("[+] Database connection established.")
        except Exception as e:
            print(f"[!] Database connection failed: {e}")
            raise

    def create_table(self):
        """Creates a table for storing log entries if it doesn't already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            log_level VARCHAR(10),
            message TEXT,
            source VARCHAR(255)
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()
        print("[+] Table 'logs' is ready.")

    def insert_log(self, log_level, message, source):
        """Inserts a log entry into the database."""
        insert_query = """
        INSERT INTO logs (log_level, message, source) 
        VALUES (%s, %s, %s);
        """
        self.cursor.execute(insert_query, (log_level, message, source))
        self.conn.commit()

    def fetch_logs(self, limit=10):
        """Fetches recent log entries from the database."""
        fetch_query = "SELECT * FROM logs ORDER BY timestamp DESC LIMIT %s;"
        self.cursor.execute(fetch_query, (limit,))
        return self.cursor.fetchall()

    def close(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()
        print("[+] Database connection closed.")
