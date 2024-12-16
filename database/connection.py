import sqlite3

from models.magazine import magazine

magazine.db = './database/magazine.db'

class Connection:
   #@staticmethod
   def get_db_connection():
        # """
        # Establishes a connection to the SQLite database.
        # Configures the connection to return rows as dictionaries.
        # """
        conn = sqlite3.connect(magazine.db)
        conn.row_factory = sqlite3.Row
        return conn
