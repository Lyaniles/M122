import mysql.connector
import pandas as pd
import json
import warnings

# Suppress pandas warning about raw DBAPI connection
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

class ScraperDB:
    def __init__(self, config_path="config.json", config_dict=None):
        # Load config to get DB credentials
        if config_dict:
            self.config = config_dict
        else:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}

        self.db_config = {
            'user': self.config.get('db_user', 'root'),
            'password': self.config.get('db_password', ''),
            'host': self.config.get('db_host', 'localhost'),
            'database': self.config.get('db_name', 'google_scraper')
        }
        
        # Determine if we need to create the DB first
        self._ensure_database_exists()
        
        # Connect to the specific database
        self.conn = mysql.connector.connect(**self.db_config)
        self.create_table()

    def _ensure_database_exists(self):
        """Connects to server without DB selected to create DB if missing."""
        try:
            temp_config = self.db_config.copy()
            del temp_config['database']
            conn = mysql.connector.connect(**temp_config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            conn.close()
        except Exception as e:
            print(f"Database creation warning (check credentials): {e}")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INT AUTO_INCREMENT PRIMARY KEY,
                search_query TEXT,
                title TEXT,
                url VARCHAR(255),
                description TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        cursor.close()

    def insert_lead(self, query, title, url, description):
        """Inserts a lead if the URL does not already exist."""
        cursor = self.conn.cursor()
        
        # Check for duplicates based on URL
        # Note: In MariaDB/MySQL we use %s for placeholders
        cursor.execute("SELECT id FROM leads WHERE url = %s", (url,))
        if cursor.fetchone() is None:
            sql = "INSERT INTO leads (search_query, title, url, description) VALUES (%s, %s, %s, %s)"
            val = (query, title, url, description)
            cursor.execute(sql, val)
            self.conn.commit()
            cursor.close()
            return True
        
        cursor.close()
        return False

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