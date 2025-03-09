from fuzzywuzzy import fuzz

# Define your language dictionary
language_dict = {'en': 'english', 'ml': 'malayalam', 'de': 'german', 'fr': 'french', 'es': 'spanish'}


# Function to extract the language from the input statement
def extract_language(input_statement):
    # Convert the input statement to lowercase for case-insensitive matching
    input_statement = input_statement.lower()

    # Initialize variables to store the detected language and the best match score
    detected_language = None
    best_match_score = 0

    # Iterate through the language dictionary and perform fuzzy matching
    for code, language in language_dict.items():
        # Calculate the fuzzy match score for both the code and the full language name
        code_score = fuzz.ratio(code, input_statement)
        language_score = fuzz.ratio(language, input_statement)

        # Choose the higher of the two scores
        max_score = max(code_score, language_score)

        # Update the detected language if this is the best match so far
        if max_score > best_match_score:
            detected_language = language
            best_match_score = max_score

    return detected_language


# Input statement from the user
input_statement = input("Enter your statement: ")

# Extract the language from the input statement
language = extract_language(input_statement)

if language:
    print(f"The detected language is: {language}")
else:
    print("Language not detected in the input statement.")
