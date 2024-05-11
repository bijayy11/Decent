import sqlite3

def connect_to_database():
    return sqlite3.connect('database.db')

def create_table():
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hashtable
                 (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

def insert_key_value(key, value):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO hashtable (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_value(key):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute("SELECT value FROM hashtable WHERE key=?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

if __name__ == "__main__":
    print(0)
