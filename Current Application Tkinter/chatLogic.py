import random
import json
import torch
import googletrans
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from fuzzywuzzy import fuzz
from texttTranslate import detect_language_full_name, translate_text
from gtts import gTTS
import os
from playsound import playsound


translation_story_level = -1
translation_flag = False

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constants
BOT_NAME = config["bot_name"]
PREFERRED_LANGUAGE = config["preferred_language"]
IDK_RESPONSES = config["idk_responses"]
CHANGE_IN_LANGUAGE_RESPONSES = config["change_in_language_responses"]
REQUEST_FOR_LANGUAGE = config["request_for_language"]
LANGUAGE_DETECT_ERROR_HANDLE = config["language_detect_error_handle"]
FILE = "data.pth"



# Load intents and model
with open('intents.json', 'r') as f:
    intents = json.load(f)

data = torch.load(FILE)
input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()


# Function to generate a random response from an intent
def generate_random_response(intent_tag):
    for intent in intents["intents"]:
        if intent_tag == intent["tag"]:
            return random.choice(intent['responses'])
    return None


# Function to process user input
def process_user_input(user_input):
    sentence = tokenize(user_input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    return tag, prob


# Function to extract the language from the input statement
def extract_language(input_statement):
    # Define your language dictionary
    language_dict = googletrans.LANGUAGES
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

# Function to translate and speak
def translate_and_speak( text, language_code):
    tts = gTTS(text=text, lang=language_code)
    tts.save("translated_text.mp3")

def play_audio():
    try:
        playsound("translated_text.mp3")
        os.remove("translated_text.mp3")
    except:
        pass


def display_and_speak_translated_text( translated_text, language_name):
    try:
        languageCodeDict = googletrans.LANGUAGES
        preferred_language_code = list(languageCodeDict.keys())[list(languageCodeDict.values()).index(language_name.lower())]
    except KeyError:
        respond = (random.choice(LANGUAGE_DETECT_ERROR_HANDLE))
        return respond

    translate_and_speak(translated_text, preferred_language_code)


def run_chat(sentence):

    global translation_flag
    global translation_story_level
    global user_text
    global new_preference_lang
    global tag

    if translation_flag is False:
        tag, prob = process_user_input(sentence)

        if prob.item() > 0.75:
            response = generate_random_response(tag)
            if tag == "translateRequest":
                translation_flag = True
            """
            if tag == "goodbye":
                quit()
            """

    if translation_flag is True:
        translation_story_level += 1

        if translation_story_level == 1:
            user_text = sentence
            response = f"The text you provided is: '{user_text}'. Is this correct?"

        elif translation_story_level == 2:
            tag, prob = process_user_input(sentence)
            if tag == "yes" and prob.item() > 0.75:
                detected_language_code, detected_language_name = detect_language_full_name(user_text)
                response = f"The detected language is {detected_language_name}. Is this correct?"
            elif tag == "no" and prob.item() > 0.75:
                response = random.choice(IDK_RESPONSES)
                translation_story_level = 0
                translation_flag = False

        elif translation_story_level == 3:
            tag, prob = process_user_input(sentence)
            if tag == "yes" and prob.item() > 0.75:
                response = f"According to your language preferences, it's in {PREFERRED_LANGUAGE}. Do you want to continue with that?"
            elif tag == "no" and prob.item() > 0.75:
                response = "Sorry, I couldn't understand the language. Please rephrase your request."
                translation_story_level = 0
                translation_flag = False

        elif translation_story_level == 4:
            tag, prob = process_user_input(sentence)
            if tag == "yes" and prob.item() > 0.75:
                response = generate_random_response(tag)+" "+"Here you go: "+translate_text(user_text, PREFERRED_LANGUAGE)
                display_and_speak_translated_text(translate_text(user_text, PREFERRED_LANGUAGE),PREFERRED_LANGUAGE)
                translation_story_level = 0
                translation_flag = False
            elif tag == "no" and prob.item() > 0.75:
                response = random.choice(CHANGE_IN_LANGUAGE_RESPONSES)


        elif translation_story_level == 5:
            new_preference_lang = extract_language(sentence)
            response = f"Okay, you prefer to convert in {new_preference_lang} right?"

        elif translation_story_level == 6:
            tag, prob = process_user_input(sentence)
            if tag == "yes" and prob.item() > 0.75:
                response = f"Great, Would you like to make it the default preference?"
            elif tag == "no" and prob.item() > 0.75:
                response = "Okay, no translation will be performed."
                translation_story_level = 0
                translation_flag = False


        elif translation_story_level == 7:
            tag, prob = process_user_input(sentence)
            if tag == "yes" and prob.item() > 0.75:
                config["preferred_language"] = new_preference_lang
                with open('config.json', 'w') as file:
                    json.dump(config, file, indent=2)
                response_addon = f"Okay, I have set {new_preference_lang} as the default language preference."
                response = response_addon + " " + "And, Here you go: " + translate_text(user_text, new_preference_lang)
                display_and_speak_translated_text(translate_text(user_text, new_preference_lang), new_preference_lang)
                translation_flag = False
                translation_story_level = 0
            elif tag == "no" and prob.item() > 0.75:
                response_addon = generate_random_response(tag)
                response = response_addon + " " + "And, Here you go: " + translate_text(user_text, new_preference_lang)
                display_and_speak_translated_text(translate_text(user_text, new_preference_lang), new_preference_lang)
                translation_flag = False
                translation_story_level = 0

    return response, translation_story_level, tag

