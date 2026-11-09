# test_sqli.py
from sqli_lab import *

def test_login_injection_blocked():
    conn = init_db()
    assert login_safe(conn, "alice' --", "wrong") is None
    assert login_safe(conn, "alice", "hash_a") == (1, "admin")

def test_search_injection_blocked():
    conn = init_db()
    assert search_safe(conn, "%' UNION SELECT id, password_hash FROM users --") == []

def test_sort_allowlist():
    conn = init_db()
    try:
        list_users(conn, "id; DROP TABLE users")
        assert False, "should have raised"
    except ValueError:
        pass
if __name__ == "__main__":
    test_login_injection_blocked()
    test_search_injection_blocked()
    test_sort_allowlist()
    print("all 3 tests passed")
