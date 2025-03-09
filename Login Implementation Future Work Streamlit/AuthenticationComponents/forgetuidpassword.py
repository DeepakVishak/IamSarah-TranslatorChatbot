import streamlit as st
from datetime import date
import bcrypt  # Import bcrypt for password hashing
from TranslatorDatabase import database, localdataservices
import time
import re

# Store OTP and user data in a dictionary for this example
otp_data = {}
user_data = {}

def generate_otp():
    return "12345"  # Replace with your OTP generation logic

def resend_otp(attempts):
    if attempts < 3:
        otp = generate_otp()
        otp_data[user_id] = otp
        return otp
    else:
        return "Attempts are over. Try again after some time."


def callback():
    st.session_state.button_clicked = True
    
def is_valid_email(email):
    # Regular expression for a basic email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+$'
    return re.match(email_regex, email) is not None

def mainpage():
    st.title("Forgot User name/Password Recovery ")

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    # Input fields for UserID recovery
    min_date = date(1920, 1, 1)
    max_date = date.today()
    dob = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)
    email = st.text_input("Email")

    # Submit button
    if st.button("Submit", on_click = callback) or st.session_state.button_clicked:
        if not dob or not email:
            st.error("Please fill in all the required fields.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:
            
            # You can add logic here to send the UserID to the user's email.
            username = database.get_key_by_email_and_dob(email,str(dob))
            field_to_fetch = ["recovery_question_index"]
            recovery_question_index = database.fetch_user_fields(username,field_to_fetch)
            
            recovery_question_index_value = list(recovery_question_index.values())[0]
            recovery_question = localdataservices.get_recovery_question(recovery_question_index_value)
            answer = st.text_input(recovery_question)

            
            if st.button("Proceed Recovery", on_click = callback) or st.session_state.button_clicked:
                # Radio buttons for password recovery options
                field_to_fetch = ["recovery_answer"]
                answer_from_server = database.fetch_user_fields(username,field_to_fetch)
                answer_from_server_extract = list( answer_from_server.values())[0]
                hashed_input_answer = database.hash_password(answer)
                
                
                
                if bcrypt.checkpw(answer.encode('utf-8'), answer_from_server_extract.encode('utf-8')):
                    recovery_option = st.radio("Select an option:", ["Forget UserID","Forget Password"], index = None)
                                   
                    
                    if recovery_option == "Forget UserID":
                        subject = "User name of your account in Application"
                        content = "Your user name is <b style='font-size: 32px;'>DeepakVishak</b>"
                        localdataservices.send_email(email, username, subject, content)
                        st.success("User name has been sent to your email.")

                    if recovery_option == "Forget Password":
                        new_password = st.text_input("New Password", type="password")
                        confirm_new_password = st.text_input("Confirm New Password", type="password")

                        if st.button("Change Password"):
                            if new_password == confirm_new_password:
                                new_password_hased = database.hash_password(new_password)
                                database.insert_user_fields(username, {"password":new_password_hased})
                                st.success("Password has been changed.")
                            else:
                                st.error("New Password and Confirm New Password do not match. Please try again.")
                else:
                    st.error("The recovery answer doesn't match with one given before!!! Please contact our support team to recover")
                    


