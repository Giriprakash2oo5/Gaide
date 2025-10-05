import streamlit as st
from login_module import init_user_db, user_portal

st.set_page_config(page_title="GAIDE Login")
st.title("🔑 GAIDE Login / Registration")

# Initialize DB
init_user_db()

# Sidebar login/register form
user_portal()

# Once logged in, store session state
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.success(f"Welcome {st.session_state['username']} (Class {st.session_state['class']})")
