import redis

records_expiration = 120

r = redis.Redis(
    host="localhost", port=9000, db=0, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"
)


def save_record(email, code):
    return r.set(email, code, ex=records_expiration)


def evaluate_code(email, code):
    return True
    # conn = sqlite3.connect(db_name)
    # c = conn.cursor()
    # c.execute(
    #     "SELECT id, email, code FROM records WHERE email=? AND code=?", (email, code)
    # )
    # results = c.fetchall()
    # if len(results) == 0:
    #     return False
    # else:
    #     return True
