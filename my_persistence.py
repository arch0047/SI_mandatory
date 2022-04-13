import sqlite3

def createDB(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, email char(100) NOT NULL, code INTEGER(4) NOT NULL)")

def save_record(db_name, email, code):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO records (email,code) VALUES (?,?)", (email,code))
    new_id = c.lastrowid
    print(f'Just saved record with ID: {new_id}')
    conn.commit()
    c.close()

def save_record(db_name, email, code):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO records (email,code) VALUES (?,?)", (email,code))
    new_id = c.lastrowid
    print(f'Just saved record with ID: {new_id}')
    conn.commit()
    c.close()