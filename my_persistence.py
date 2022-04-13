import sqlite3


def createDB(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, email char(100) NOT NULL, code INTEGER(4) NOT NULL)"
    )


def save_record(db_name, email, code):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO records (email,code) VALUES (?,?)", (email, code))
    new_id = c.lastrowid
    conn.commit()
    c.close()


def evaluate_code(db_name, email, code):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        "SELECT id, email, code FROM records WHERE email=? AND code=?", (email, code)
    )
    results = c.fetchall()
    if len(results) == 0:
        return False
    else:
        return True
