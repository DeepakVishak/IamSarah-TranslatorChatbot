import streamlit as st
from googletrans import LANGUAGES
import re

# Extract the language names from the LANGUAGES dictionary
google_languages = [lang.capitalize() for lang in LANGUAGES.values()]

# Streamlit app title
st.title("Create an Account")

# Input fields for user registration
username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
dob = st.date_input("Date of Birth")
email = st.text_input("Email")
language_preference = st.selectbox("Language Preference", google_languages)

# Create an "Create Account" button
if st.button("Create Account"):
    # Validation for mandatory fields
    if not (username and password and confirm_password and dob and email and language_preference):
        st.error("Please fill in all the mandatory fields.")
    # Email validation
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Invalid email address. Please enter a valid email.")
    # Password match validation
    elif password != confirm_password:
        st.error("Password and Confirm Password do not match.")
    else:
        # Registration logic can be added here (e.g., storing user data, etc.)
        st.success("Account created successfully! You can now log in.")
