import hashlib
import hmac
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

def sha(p):
    # Demo only. Real apps use bcrypt or argon2 with a per-user salt.
    return hashlib.sha256(p.encode()).hexdigest()

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(f"""
    CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT,
                        password_hash TEXT, role TEXT);
    INSERT INTO users (username, password_hash, role) VALUES
      ('alice', '{sha("alicepass")}', 'admin'),
      ('bob',   '{sha("bobpass")}',   'user');
""")

@app.get("/")
def home():
    return "CyberShield demo is running"

# ---------- VULNERABLE ----------
@app.post("/login-vulnerable")
def login_vulnerable():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    q = (f"SELECT id, username, role FROM users "
         f"WHERE username = '{username}' AND password_hash = '{sha(password)}'")
    try:
        row = db.execute(q).fetchone()
    except sqlite3.Error as e:
        # Also a bug, on purpose: echoing errors and the query helps attackers.
        return jsonify(error=str(e), query=q), 500
    if row:
        return jsonify(status="logged in", id=row[0], user=row[1], role=row[2])
    return jsonify(status="denied"), 401

# ---------- FIXED ----------
@app.post("/login-safe")
def login_safe():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    row = db.execute(
        "SELECT id, username, role, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if row and hmac.compare_digest(row[3], sha(password)):
        return jsonify(status="logged in", id=row[0], user=row[1], role=row[2])
    return jsonify(status="denied"), 401   # same generic answer for every failure

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)   # never debug=True: it exposes a code console
