import streamlit as st
import re
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            email TEXT,
            password TEXT
            )""")
conn.commit()

# App title
st.title("Registration Form")

# Form header
st.header("Please complete your information")

name = st.text_input("Full Name:")
email = st.text_input("Email:")
password = st.text_input("Password:", type="password")

# Email validation function
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Register button
if st.button("Register"):
    if name and email and password:
        if validate_email(email):
            # Save data to database
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            st.success("Registration successful!")
        else:
            st.error("Invalid email address. Please enter a valid email.")
    else:
        st.error("All fields must be filled out!")

# Show registered users (optional)
if st.checkbox("Show registered users"):
    st.subheader("User List")
    c.execute("SELECT name, email FROM users")
    users = c.fetchall()
    for user in users:
        st.write(f"Name: {user[0]}, Email: {user[1]}")
