import streamlit as st
from TranslatorDatabase import database
import bcrypt

def mainpage():
    st.title("Welcome to the Login Page")

    # Input fields for user ID and password
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if user_id and password:
            check_username_result, check_username_password = database.check_username(user_id)
            if check_username_result == True:
                if bcrypt.checkpw(password.encode('utf-8'), check_username_password.encode('utf-8')):
                    st.success("Login Successful!")
                else:
                    st.error("Login Failed. Please check your credentials.")
            else:
                st.error("Login Failed. Given UserID doesnot exist.")
        else:
            st.error("Please fill in both User ID and Password fields.")
