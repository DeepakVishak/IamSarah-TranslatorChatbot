from deta import Deta
import bcrypt
import json
from decouple import config
import os
import json


# Load the Deta project key from the .env file
DETA_KEY = config('DETA_KEY')


# Initialize with a project key
deta = Deta(DETA_KEY)


#This is how to create/connect a database
db = deta.Base("UserProfile")


#Functionalities

def load_recovery_questions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'TranslatorDatabase', 'recovery_questions.json')
    
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data.get('questions', [])

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_user_data(username, password, date_of_birth, email, recovery_question, recovery_answer, language_code):
    # Hash the password and recovery answer using bcrypt
    hashed_password = hash_password(password)
    hashed_recovery_answer = hash_password(recovery_answer)

    # Load recovery questions from Deta
    recovery_questions = load_recovery_questions()

    # Find the index of the selected recovery question
    recovery_question_index = recovery_questions.index(recovery_question)

    # Create the dictionary
    user_data = {
        "key": username,
        "password": hashed_password,  # Convert bytes to string
        "date_of_birth": str(date_of_birth),
        "email": email,
        "recovery_question_index": recovery_question_index,
        "recovery_answer": hashed_recovery_answer,
        "preferred_language_code": language_code
    }

    result = db.put(user_data)

    if result:
        return True
    else:
        return False

def check_username(username):
    try:
        user_data = db.get(username)
        if user_data is not None:
            return (True, user_data.get('password', ''))
        else:
            return (False, '')
    except Exception as e:
        print(f"Error while checking username: {e}")
        return (False, '')


def retrieve_user_data(username, json_file_path):
    try:
        user_data = db.get(username)
        if user_data is not None:
            # Define which fields to exclude
            exclude_fields = ["password", "recovery_answer"]

            # Create a new dictionary with excluded fields
            user_data_filtered = {key: value for key, value in user_data.items() if key not in exclude_fields}

            # Write the user data to the specified JSON file
            with open(json_file_path, 'w') as file:
                json.dump(user_data_filtered, file, indent=4)

            return True
        else:
            return False
    except Exception as e:
        print(f"Error while retrieving user data: {e}")
        return False

def insert_user_fields(username, data_dict):
    try:
        user_data = db.get(username)

        if user_data is None:
            user_data = {}  # If the user doesn't exist, create an empty user_data dictionary.

        for attribute, value in data_dict.items():
            user_data[attribute] = value

        db.put(user_data, key=username)  # Save the user_data dictionary with the username as the key.

        return True  # Data insertion was successful.
    except Exception as e:
        print(f"Error while inserting user fields: {e}")
        return False  # Data insertion failed.

def fetch_user_fields(username, fields_to_fetch):
    try:
        user_data = db.get(username)
        if user_data is not None:
            user_fields = {}
            for field in fields_to_fetch:
                if field in user_data:
                    user_fields[field] = user_data[field]

            return user_fields
        else:
            return None
    except Exception as e:
        print(f"Error while fetching user fields: {e}")
        return None


def find_username_by_email(email):
    try:
        # Fetch user data with the provided email and convert it to a list
        user_data_list = list(db.fetch({"email": email}))

        if user_data_list:
            # Iterate through the list to find the username (key) associated with the email
            for user_data in user_data_list:
                return user_data["key"]
        return None  # Return None if the email is not found
    except Exception as e:
        print(f"Error while finding username by email: {e}")
        return None

def authenticate_user(email, dob):
    try:
        # Find the username (key) associated with the provided email
        username = find_username_by_email(email)

        if username:
            # Fetch the user's data from the server
            user_data = db.get(username)

            if user_data is not None:
                # Check if the provided date of birth matches the stored date of birth
                if user_data.get('date_of_birth') == dob:
                    return username  # Return the username (key) if the date of birth matches
        return None  # Return None if authentication fails
    except Exception as e:
        print(f"Error while authenticating user: {e}")
        return None


def check_email(email):
    try:
        # Iterate through the user data to check if the provided email exists
        for user_data in db.fetch({"email": email}).items:
            return True  # Return True if the email exists
        return False  # Return False if the email does not exist
    except Exception as e:
        print(f"Error while checking email: {e}")
        return False

def get_key_by_email_and_dob(email_to_find, dob_to_find):
    try:
        # Fetch the item with the specified email
        item = db.fetch({"email": email_to_find}).items[0]

        # Check if the email and DOB match
        if item.get("email") == email_to_find and item.get("date_of_birth") == dob_to_find:
            return item.get("key")
        else:
            return None
    except IndexError:
        # IndexError is raised when no item with the specified email is found
        return None
    except Exception as e:
        print(f"Error while getting key by email and DOB: {e}")
        return None



