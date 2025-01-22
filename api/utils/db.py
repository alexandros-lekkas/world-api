import sqlite3

def connect_db(db_path: str):
    """
    Connect to the database and return a connection object.
    
    Args:
        db_path (str): The path to the SQLite database file.
        
    Returns (sqlite3.Connection): A connection object to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    return conn
