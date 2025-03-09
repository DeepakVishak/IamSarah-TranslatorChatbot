import streamlit as st
import re
from datetime import datetime

# Function to validate the email format
def is_valid_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+$'
    return re.match(email_pattern, email)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'authenticated_email' not in st.session_state:
    st.session_state.authenticated_email = None

st.title("User Authentication")

email = st.text_input("Enter Email")
dob = st.date_input("Enter Date of Birth")

if st.button("Submit"):
    if email.strip() == "" or dob is None:
        st.error("Both fields are mandatory.")
    elif email == "test@email.com" and dob.strftime('%d/%m/%Y') == "01/01/2014":
        st.success("Authentication successful!")
        st.session_state.authenticated = True
        st.session_state.authenticated_email = email
    else:
        st.error("Enter correct credentials")

if st.session_state.authenticated:
    if st.button("Change Password"):
        st.write(f"Changing password for email: {st.session_state.authenticated_email}")
        # These fields are inside the "Change Password" section
        password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Update Password"):
            if password == confirm_password:
                # Add code to handle password update here
                st.success("Password updated successfully!")
            else:
                st.error("Passwords do not match. Please try again.")
