import streamlit as st

# Define the title of your login page
st.title("Login Page")

# Create input fields for user ID and password
user_id = st.text_input("User ID")
password = st.text_input("Password", type="password")

# Create a login button
if st.button("Login"):
    # Check if the user entered a valid user ID and password
    if user_id == "your_username" and password == "your_password":
        st.success("Login successful!")
    else:
        st.error("Login failed. Please check your credentials.")
