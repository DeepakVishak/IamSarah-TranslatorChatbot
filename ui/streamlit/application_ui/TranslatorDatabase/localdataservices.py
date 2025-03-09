import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
import random
import json
import os
from TranslatorDatabase import database

def send_email( receiver_email, receiver_name, subject, content):
    try:

        GOOGLE_KEY = config('GOOGLE_KEY')
        sender_email = "deepak474700@gmail.com"
        sender_password = GOOGLE_KEY
        
        # Create a MIMEText object to represent the email content with HTML formatting
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add the recipient's name and HTML-formatted content to the email
        html_content = f"Hello, {receiver_name}!<br><br>{content}"
        message.attach(MIMEText(html_content, "html"))

        # Establish a connection to the SMTP server (in this case, Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Login to your Gmail account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Close the SMTP server connection
        server.quit()

        print("Email sent successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def generate_otp():
    # Generate a random 4-digit OTP
    otp = random.randint(1000, 9999)
    return otp

def get_recovery_question(index):
    recovery_questions = database.load_recovery_questions()
    return recovery_questions[index]







"""
receiver_email = "deepakvishak@outlook.com"
receiver_name = "Recipient Name Test"
subject = "Your Email Subject Test"
content = "Your user name is <b style='font-size: 32px;'>DeepakVishak</b>"

send_email( receiver_email, receiver_name, subject, content)
"""
