import mysql.connector
import pandas as pd
import warnings
from src.utils import load_config

# Suppress pandas warning about raw DBAPI connection
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

class ScraperDB:
    def __init__(self, config_path="config.json", config_dict=None):
        # Load config to get DB credentials
        if config_dict:
            self.config = config_dict
        else:
            self.config = load_config()

        self.db_config = {
            'user': self.config.get('db_user', 'root'),
            'password': self.config.get('db_password', ''),
            'host': self.config.get('db_host', 'localhost'),
            'database': self.config.get('db_name', 'google_scraper')
        }
        
        # Determine if we need to create the DB first
        self._ensure_database_exists()
        
        # Connect to the specific database
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.create_table()
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            self.conn = None # Ensure conn is None if connection fails

    def _ensure_database_exists(self):
        """Connects to server without DB selected to create DB if missing."""
        try:
            temp_config = self.db_config.copy()
            del temp_config['database']
            conn = mysql.connector.connect(**temp_config)
            cursor = conn.cursor()
            # Use parameterized query to prevent SQL injection
            cursor.execute("CREATE DATABASE IF NOT EXISTS %s", (self.db_config['database'],))
            conn.close()
        except mysql.connector.Error as e:
            print(f"Database creation warning (check credentials): {e}")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INT AUTO_INCREMENT PRIMARY KEY,
                search_query TEXT,
                title TEXT,
                url VARCHAR(767) UNIQUE,
                description TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        cursor.close()

    def insert_lead(self, query, title, url, description):
        """Inserts a lead and returns True if successful, False on duplicate."""
        cursor = self.conn.cursor()
        sql = "INSERT INTO leads (search_query, title, url, description) VALUES (%s, %s, %s, %s)"
        val = (query, title, url, description)
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            return True
        except mysql.connector.IntegrityError:
            # This occurs if the URL is a duplicate
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def fetch_all(self):
        """Returns all leads as a Pandas DataFrame."""
        return pd.read_sql("SELECT * FROM leads ORDER BY scraped_at DESC", self.conn)

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()