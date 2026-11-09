from sqli_lab import *

conn = init_db()

#part 1: shows why ? cant be used for a column name
print(conn.execute("SELECT id, username FROM users ORDER BY ?", ("username",)).fetchall())
print(conn.execute("SELECT id, username FROM users ORDER BY ?", ("id DESC",)).fetchall())

#part 3: the allowlist in action
for s in ["id", "username", "username; DROP TABLE users", "password_hash"]:
    try:
        print(s, "->", list_users(conn, s))
    except ValueError as e:
        print(s, "->", "rejected:", e)
