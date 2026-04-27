import sqlite3
from datetime import datetime
import atexit
FILE_DB = "app_data.db"

_connection = None

def connect():
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(FILE_DB)
        _connection.row_factory = sqlite3.Row

        _connection.execute("PRAGMA journal_mode=WAL;")
        _connection.execute("PRAGMA synchronous=NORMAL;")

    return _connection


def close_connection():
    global _connection
    if _connection:
        _connection.close()

atexit.register(close_connection)

def setup():
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    interferer.execute("""
        CREATE TABLE IF NOT EXISTS goals(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            goal_name TEXT,
            target_amount INTEGER,
            nominal_per_box INTEGER,
            created_at TEXT
        )
    """)

    interferer.execute("""
        CREATE TABLE IF NOT EXISTS goal_boxes(
            id INTEGER PRIMARY KEY,
            goal_id INTEGER,
            box_index INTEGER,
            checked INTEGER DEFAULT 0
        )
    """)

    connection.commit()


def get_user_by_id(user_id: int):
    connection = connect()
    interferer = connection.cursor()
    interferer.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return interferer.fetchone()

def register_user(username: str, password: str):
    connection = connect()
    interferer = connection.cursor()
    interferer.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username.replace(" ", ""), password.replace(" ", ""))
    )
    connection.commit()


def login_user(username, password):
    connection = connect()
    interferer = connection.cursor()
    interferer.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password)
    )
    current_user = interferer.fetchone()
    return current_user["id"] if current_user else None


def delete_user(user_id):
    connection = connect()
    interferer = connection.cursor()
    interferer.execute("DELETE FROM users WHERE id=?", (user_id,))
    connection.commit()


def create_goal(user_id, name, target, nominal):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        INSERT INTO goals(user_id,goal_name,target_amount,nominal_per_box,created_at)
        VALUES(?,?,?,?,?)
    """, (user_id, name, target, nominal, datetime.now().isoformat()))

    goal_id = interferer.lastrowid
    total_boxes = target // nominal

    for i in range(total_boxes):
        interferer.execute(
            "INSERT INTO goal_boxes(goal_id,box_index,checked) VALUES (?,?,0)",
            (goal_id, i)
        )

    connection.commit()


def get_goals(user_id):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        SELECT id, goal_name, target_amount, nominal_per_box
        FROM goals WHERE user_id=?
    """, (user_id,))

    return [
        (row["id"], row["goal_name"], row["target_amount"], row["nominal_per_box"])
        for row in interferer.fetchall()
    ]


def update_goal(goal_id, name, target, nominal):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        UPDATE goals
        SET goal_name=?, target_amount=?, nominal_per_box=?
        WHERE id=?
    """, (name, target, nominal, goal_id))

    interferer.execute("DELETE FROM goal_boxes WHERE goal_id=?", (goal_id,))

    total = target // nominal
    for box_index in range(total):
        interferer.execute(
            "INSERT INTO goal_boxes(goal_id, box_index, checked) VALUES (?, ?, 0)",
            (goal_id, box_index)
        )

    connection.commit()


def delete_goal(goal_id):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("DELETE FROM goal_boxes WHERE goal_id=?", (goal_id,))
    interferer.execute("DELETE FROM goals WHERE id=?", (goal_id,))

    connection.commit()


def get_boxes(goal_id):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        SELECT box_index, checked
        FROM goal_boxes
        WHERE goal_id=?
    """, (goal_id,))

    return {row["box_index"]: row["checked"] for row in interferer.fetchall()}


def toggle_box(goal_id, index):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        UPDATE goal_boxes
        SET checked = NOT checked
        WHERE goal_id=? AND box_index=?
    """, (goal_id, index))

    connection.commit()


def count_checked(goal_id):
    connection = connect()
    interferer = connection.cursor()

    interferer.execute("""
        SELECT COUNT(*) as total
        FROM goal_boxes
        WHERE goal_id=? AND checked=1
    """, (goal_id,))

    return interferer.fetchone()["total"]

if __name__ == "__main__":
    delete_user(3)