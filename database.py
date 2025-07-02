import sqlite3
import os

DB = 'database.db'

def init_db():
    """ Initialize the SQLite database using schema.sql if the database file 
    does not exist."""
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())

def query_db(query, args=(), one=False):
    """ Execute a SQL query with optional arguments.
    Returns one row or all rows as dictionaries depending on the 'one' flag. """
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.execute(query, args)
        result = cursor.fetchall()
        conn.commit()
        return result[0] if result and one else result
