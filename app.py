import streamlit as st
import mysql.connector # type: ignore
from mysql.connector import Error
import hashlib
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='qwerty69.',
        database='user_akshit'
    )

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insert new user
def insert_user(username, email, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hash_password(password))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        st.error(f"Error: {e}")
        return False

# Authenticate user
def login_user(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, hash_password(password))
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Streamlit interface
def main():
    st.set_page_config(page_title="Login/Signup App", layout="centered")
    
    if 'page' not in st.session_state:
        st.session_state.page = "signup"

    if st.session_state.page == "signup":
        st.title("Signup Page")

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if password != confirm:
                st.warning("Passwords do not match")
            elif username and email and password:
                if insert_user(username, email, password):
                    st.success("Account created successfully!")
                    st.session_state.page = "login"
            else:
                st.warning("Please fill in all fields.")

        st.info("Already have an account? [Login here](#)", icon="ℹ️")
        if st.button("Go to Login"):
            st.session_state.page = "login"

    elif st.session_state.page == "login":
        st.title("Login Page")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.success(f"Welcome, {username}!")
                st.balloons()
                st.write("You're logged in.")
            else:
                st.error("Invalid credentials")

        st.info("Don't have an account? [Sign up here](#)", icon="ℹ️")
        if st.button("Go to Signup"):
            st.session_state.page = "signup"

if __name__ == "__main__":
    main()