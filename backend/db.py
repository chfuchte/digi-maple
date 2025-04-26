import sqlite3
from env import DB_PATH

def setup() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        with open('./sql/setup.sql', 'r') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
        conn.commit()
