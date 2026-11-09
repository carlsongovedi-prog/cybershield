# SQL Injection Demo: Vulnerable vs Fixed Code

A self-contained lab using Python's built-in `sqlite3` and an in-memory database. No installs needed.

## Setup

```python
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
```

## 1. Authentication bypass

**Vulnerable** (user input pasted into the SQL text):

```python
def login_vulnerable(conn, username, password_hash):
    q = (f"SELECT id, role FROM users "
         f"WHERE username = '{username}' AND password_hash = '{password_hash}'")
    return conn.execute(q).fetchone()
```

**Fixed** (values sent separately from the SQL):

```python
def login_safe(conn, username, password_hash):
    return conn.execute(
        "SELECT id, role FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash),
    ).fetchone()
```

**Attack:** username `alice' --`, password `wrong`. The `--` comments out the password check, so the database receives:

```sql
SELECT id, role FROM users WHERE username = 'alice' --' AND password_hash = 'wrong'
```

| Call | Output |
|---|---|
| `login_vulnerable(conn, "alice' --", "wrong")` | `(1, 'admin')` (logged in as admin with no password) |
| `login_safe(conn, "alice' --", "wrong")` | `None` |
| `login_safe(conn, "alice", "hash_a")` (legitimate login) | `(1, 'admin')` |

## 2. Data extraction with UNION

**Vulnerable:**

```python
def search_vulnerable(conn, term):
    q = f"SELECT id, username FROM users WHERE username LIKE '%{term}%'"
    return conn.execute(q).fetchall()
```

**Fixed:**

```python
def search_safe(conn, term):
    return conn.execute(
        "SELECT id, username FROM users WHERE username LIKE ?",
        (f"%{term}%",),
    ).fetchall()
```

**Attack:** `%' UNION SELECT id, password_hash FROM users --`

| Call | Output |
|---|---|
| `search_vulnerable(conn, payload)` | `[(1, 'alice'), (1, 'hash_a'), (2, 'bob'), (2, 'hash_b'), (3, 'carol'), (3, 'hash_c')]` (password hashes leaked) |
| `search_safe(conn, payload)` | `[]` |

## 3. Injection with no quote character

This shows why stripping `'` is not a fix: a numeric context needs no quotes.

**Vulnerable:**

```python
def get_user_vulnerable(conn, user_id):
    return conn.execute(f"SELECT id, username FROM users WHERE id = {user_id}").fetchall()
```

**Fixed:**

```python
def get_user_safe(conn, user_id):
    return conn.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchall()
```

| Call | Output |
|---|---|
| `get_user_vulnerable(conn, "1 OR 1=1")` | `[(1, 'alice'), (2, 'bob'), (3, 'carol')]` (every row) |
| `get_user_vulnerable(conn, "0 UNION SELECT id, password_hash FROM users")` | `[(1, 'hash_a'), (2, 'hash_b'), (3, 'hash_c')]` (hashes leaked) |
| `get_user_safe(conn, "1 OR 1=1")` | `[]` |
| `get_user_safe(conn, "0 UNION SELECT id, password_hash FROM users")` | `[]` |

## 4. Identifiers cannot be parameterized: use an allowlist

A `?` placeholder only binds values, never column names. `ORDER BY ?` silently does nothing. Map the user's choice through a fixed allowlist and put only your own hard-coded names into the SQL.

```python
ALLOWED_SORT = {"id": "id", "username": "username"}

def list_users(conn, sort="id"):
    col = ALLOWED_SORT.get(sort)
    if col is None:
        raise ValueError("invalid sort column")
    return conn.execute(f"SELECT id, username FROM users ORDER BY {col}").fetchall()
```

| Input | Output |
|---|---|
| `"id"` | `[(1, 'alice'), (2, 'bob'), (3, 'carol')]` |
| `"username"` | `[(1, 'alice'), (2, 'bob'), (3, 'carol')]` |
| `"username; DROP TABLE users"` | rejected: `invalid sort column` |
| `"password_hash"` (real column, not allowlisted) | rejected: `invalid sort column` |

## Takeaways

1. **Parameterize every value.** Use `?` in sqlite3 and `%s` in the MySQL/Postgres drivers. Never use f-strings, `+`, or `.format()` to build queries from input.
2. **Blocklists fail.** Injection works without quotes (section 3), filters get bypassed, and they break legitimate input such as O'Brien.
3. **Allowlist identifiers.** Attacker-controlled text never reaches the query, and unlisted columns stay unreachable.
4. **Defense in depth.** Give the database user minimal privileges, hash passwords with bcrypt or argon2, and never return raw database errors to users.

## Finding injection in a real codebase

```bash
grep -rnE "execute\(\s*f[\"']" --include=*.py .
grep -rnE "execute\(.*(\.format\(|%\s*\(|\+\s*\w+)" --include=*.py .
```

This is a triage list, not a guarantee. Review each hit, and also check ORM escape hatches such as `text()`, `.raw()`, and `.extra()`.
