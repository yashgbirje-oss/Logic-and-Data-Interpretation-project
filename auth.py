import sqlite3, hashlib, hmac, json, secrets, re
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import streamlit as st

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"
USER_RE = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
DEFAULT_ADMIN = ("admin", "admin123")


@contextmanager
def _db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _hash(password, salt_hex):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 120_000).hex()


def _admin_credentials():
    try:
        return st.secrets["ADMIN_USERNAME"], st.secrets["ADMIN_PASSWORD"]
    except Exception:
        return DEFAULT_ADMIN


def init_db():
    with _db() as c:
        c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, salt TEXT, pw_hash TEXT, role TEXT, full_name TEXT, created TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS progress(username TEXT PRIMARY KEY, data TEXT)")
        n = c.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0]
    if n == 0:
        u, p = _admin_credentials()
        create_user(u, p, "admin", "Administrator", check=False)


def create_user(username, password, role="user", full_name="", check=True):
    username = username.strip().lower()
    if check and not USER_RE.match(username):
        return False, "Username must be 3-30 characters: letters, numbers, . _ -"
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if role not in ("admin", "user"):
        return False, "Invalid role."
    salt = secrets.token_hex(16)
    try:
        with _db() as c:
            c.execute("INSERT INTO users VALUES(?,?,?,?,?,?)",
                      (username, salt, _hash(password, salt), role, full_name.strip(), datetime.now().strftime("%Y-%m-%d %H:%M")))
    except sqlite3.IntegrityError:
        return False, "That username already exists."
    return True, f"User '{username}' created."


def verify(username, password):
    with _db() as c:
        r = c.execute("SELECT * FROM users WHERE username=?", (username.strip().lower(),)).fetchone()
    if r and hmac.compare_digest(r["pw_hash"], _hash(password, r["salt"])):
        return {"username": r["username"], "role": r["role"], "full_name": r["full_name"]}
    return None


def list_users():
    with _db() as c:
        return [dict(r) for r in c.execute("SELECT username, full_name, role, created FROM users ORDER BY role, username")]


def set_password(username, password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    salt = secrets.token_hex(16)
    with _db() as c:
        c.execute("UPDATE users SET salt=?, pw_hash=? WHERE username=?", (salt, _hash(password, salt), username))
    return True, "Password updated."


def set_role(username, role):
    with _db() as c:
        if role != "admin" and c.execute("SELECT COUNT(*) FROM users WHERE role='admin' AND username<>?", (username,)).fetchone()[0] == 0:
            return False, "There must be at least one admin."
        c.execute("UPDATE users SET role=? WHERE username=?", (role, username))
    return True, "Role updated."


def delete_user(username):
    with _db() as c:
        r = c.execute("SELECT role FROM users WHERE username=?", (username,)).fetchone()
        if r and r["role"] == "admin" and c.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0] <= 1:
            return False, "Cannot delete the last admin."
        c.execute("DELETE FROM users WHERE username=?", (username,))
        c.execute("DELETE FROM progress WHERE username=?", (username,))
    return True, f"User '{username}' deleted."


def load_progress(username):
    with _db() as c:
        r = c.execute("SELECT data FROM progress WHERE username=?", (username,)).fetchone()
    try:
        return json.loads(r["data"]) if r else {}
    except Exception:
        return {}


def save_progress(username, data):
    with _db() as c:
        c.execute("INSERT INTO progress VALUES(?,?) ON CONFLICT(username) DO UPDATE SET data=excluded.data",
                  (username, json.dumps(data)))


def export_all():
    with _db() as c:
        users = [dict(r) for r in c.execute("SELECT * FROM users")]
        prog = {r["username"]: json.loads(r["data"]) for r in c.execute("SELECT * FROM progress")}
    return json.dumps({"users": users, "progress": prog}, indent=2)


def import_all(text):
    d = json.loads(text)
    with _db() as c:
        for u in d.get("users", []):
            c.execute("INSERT OR REPLACE INTO users VALUES(?,?,?,?,?,?)",
                      (u["username"], u["salt"], u["pw_hash"], u["role"], u.get("full_name", ""), u.get("created", "")))
        for name, data in d.get("progress", {}).items():
            c.execute("INSERT OR REPLACE INTO progress VALUES(?,?)", (name, json.dumps(data)))
    return len(d.get("users", []))
