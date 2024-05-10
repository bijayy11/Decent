import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
      host='host',
        user='username',
        password='password',
        database='schema'
    )
def create_table():
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hashtable
                 (key VARCHAR(255) PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()


def insert_key_value(key, value):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT INTO hashtable (key, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value = %s", (key, value, value))
    conn.commit()
    conn.close()

def get_value(key):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute("SELECT value FROM hashtable WHERE key=%s", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None



