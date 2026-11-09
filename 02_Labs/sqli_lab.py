import sqlite3

def init_db():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT,
                            password_hash TEXT, role TEXT);
        INSERT INTO users (username, password_hash, role) VALUES
          ('alice', 'hash_a', 'admin'),
          ('bob',   'hash_b', 'user'),
          ('carol', 'hash_c', 'user');
    """)
    return conn

# ---------- VULNERABLE ----------
def login_vulnerable(conn, username, password_hash):
    q = (f"SELECT id, role FROM users "
         f"WHERE username = '{username}' AND password_hash = '{password_hash}'")
    return conn.execute(q).fetchone()

def search_vulnerable(conn, term):
    q = f"SELECT id, username FROM users WHERE username LIKE '%{term}%'"
    return conn.execute(q).fetchall()

def get_user_vulnerable(conn, user_id):
    return conn.execute(f"SELECT id, username FROM users WHERE id = {user_id}").fetchall()

# ---------- FIXED ----------
def login_safe(conn, username, password_hash):
    return conn.execute(
        "SELECT id, role FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash),
    ).fetchone()

def search_safe(conn, term):
    return conn.execute(
        "SELECT id, username FROM users WHERE username LIKE ?",
        (f"%{term}%",),
    ).fetchall()

def get_user_safe(conn, user_id):
    return conn.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchall()

# Identifiers (column names) can't be parameterized: use an allowlist.
ALLOWED_SORT = {"id": "id", "username": "username"}

def list_users(conn, sort="id"):
    col = ALLOWED_SORT.get(sort)
    if col is None:
        raise ValueError("invalid sort column")
    return conn.execute(f"SELECT id, username FROM users ORDER BY {col}").fetchall()
