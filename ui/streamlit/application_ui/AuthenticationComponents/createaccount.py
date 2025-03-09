import streamlit as st
import re
from datetime import date
import bcrypt  # Import bcrypt for password hashing
from TranslatorDatabase import database
import json
import os
import googletrans

def load_recovery_questions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'TranslatorDatabase', 'recovery_questions.json')
    
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data.get('questions', [])

def is_valid_username(username):
    # Regular expression for alphanumeric characters and no spaces
    username_regex = r'^[a-zA-Z0-9]+$'
    return re.match(username_regex, username) is not None

def is_valid_email(email):
    # Regular expression for a basic email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+$'
    return re.match(email_regex, email) is not None

def mainpage():
    st.title("Create a New Account")

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Set the date input to start from 1/1/1920
    min_date = date(1920, 1, 1)
    max_date = date.today()
    date_of_birth = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)

    email = st.text_input("Email")

    # Recovery question dropdown
    recovery_questions = load_recovery_questions()
    recovery_question = st.selectbox("Recovery Question", recovery_questions)

    recovery_answer = st.text_input("Recovery Question Answer", type="password")

    # Preferred Language selection
    language_names = [name.capitalize() for name in googletrans.LANGUAGES.values()]
    selected_language = st.selectbox("Preferred Language", language_names)

    # Get the language code corresponding to the selected language name
    language_code = [k for k, v in googletrans.LANGUAGES.items() if v.lower() == selected_language.lower()][0]

    #Check if username already exists
    check_username_result, _ = database.check_username(username)

    #Check if email already exists
    check_email_exist = database.check_email(email)



    # Validation
    if st.button("Submit"):
        if not username or not password or not confirm_password or not date_of_birth or not email or not recovery_answer:
            st.error("Please fill in all the required fields.")
        elif password != confirm_password:
            st.error("Password and Confirm Password do not match. Please try again.")
        elif not is_valid_username(username):
            st.error("Username should be alphanumeric and not contain spaces.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif check_username_result is True:
            st.warning("The user name provided is already exists if its yours account go to Forget UserID/ Password to recover it or make another username")
        elif check_email_exist is True:
            st.warning("The email provided is already exists if its yours account go to Forget UserID/ Password to recover it or use another email ID")
        else:
            # Call the function to create the user data dictionary
            user_data_result = database.create_user_data(username, password, date_of_birth, email, recovery_question, recovery_answer, language_code)

            # Display the output of the dictionary
            if user_data_result is True:
                st.success("New account is created")
            else:
                st.error("Failed to insert the data")
                
            


