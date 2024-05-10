import sqlite3

# Function to create a new SQLite database and table if they don't exist
def create_database():
    conn = sqlite3.connect('hashtable.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hashtable
                 (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

# Function to insert a key-value pair into the database
def insert_key_value(key, value):
    conn = sqlite3.connect('key_value_store.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO hashtable (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

# Function to retrieve a value by key from the database
def get_value(key):
    conn = sqlite3.connect('key_value_store.db')
    c = conn.cursor()
    c.execute("SELECT value FROM hashtable WHERE key=?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
