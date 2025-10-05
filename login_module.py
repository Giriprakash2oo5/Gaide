# login_module.py
import sqlite3
import bcrypt
import streamlit as st

DB_PATH = "users.db"

# ---------- DB Setup ----------
def init_user_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB,
            class TEXT
        )
        """
    )
    conn.commit()
    conn.close()

# ---------- Password Utils ----------
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed)
    except Exception:
        return False

# ---------- DB Functions ----------
def register_user(username: str, password: str, user_class: str) -> bool:
    if not username or not password:
        return False
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        c.execute(
            "INSERT INTO users (username, password, class) VALUES (?, ?, ?)",
            (username, hashed_pw, user_class),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password, class FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and check_password(password, row[0]):
        return True, row[1]
    return False, None

# ---------- UI ----------
def user_portal():
    st.sidebar.title("🔑 User Portal")
    option = st.sidebar.radio("Choose Action", ["Login", "Register"])

    if option == "Register":
        st.subheader("Create Account")
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            user_class = "12"
            if register_user(new_user, new_pass, user_class):
                st.success("✅ Account created! Please log in.")
            else:
                st.error("❌ Username already exists or invalid input.")

    elif option == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, user_class = login_user(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["class"] = user_class
                st.success(f"✅ Welcome {username}! You are in Class {user_class}.")
            else:
                st.error("❌ Invalid username or password.")
