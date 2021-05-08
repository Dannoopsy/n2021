import sqlite3


PATH_GOOGLE = 'drive/MyDrive/'
connection = None

def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect(PATH_GOOGLE + 'database.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    return inner





@ensure_connection
def init_db(conn, force: bool = False):
    #conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            id            INTEGER PRIMARY KEY,
            user_id       INTEGER NOT NULL,
            text          TEXT NOT NULL
        )
    
    ''')

    conn.commit()

@ensure_connection
def add_message(user_id: int, text: str, conn):
    #conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()


@ensure_connection
def count_message(user_id: int, conn):
    #conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_message WHERE user_id = ?', (user_id,))
    (res, ) = c.fetchall()
    conn.commit()
    return res


@ensure_connection
def list_message(conn, user_id: int, limit: int = 10):
    #conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()
