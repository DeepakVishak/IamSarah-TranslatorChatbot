import os
import random
import json
import torch
import pyttsx3
from gtts import gTTS
from playsound import playsound
import googletrans
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from fuzzywuzzy import fuzz
from texttTranslate import detect_language_full_name, translate_text

class ChatBotSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatBotSingleton, cls).__new__(cls)
            cls._instance.initialize_chatbot()
        return cls._instance

    def initialize_chatbot(self):
        # Load configuration
        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)

        # Constants
        self.BOT_NAME = self.config["bot_name"]
        self.PREFERRED_LANGUAGE = self.config["preferred_language"]
        self.IDK_RESPONSES = self.config["idk_responses"]
        self.CHANGE_IN_LANGUAGE_RESPONSES = self.config["change_in_language_responses"]
        self.REQUEST_FOR_LANGUAGE = self.config["request_for_language"]
        self.LANGUAGE_DETECT_ERROR_HANDLE = self.config["language_detect_error_handle"]
        self.FILE = "data.pth"

        # Initialize the pyttsx3 text-to-speech engine
        self.engine = pyttsx3.init()

        # Set the voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

        # Load intents and model
        with open('intents.json', 'r') as f:
            self.intents = json.load(f)

        self.data = torch.load(self.FILE)
        self.input_size = self.data['input_size']
        self.hidden_size = self.data['hidden_size']
        self.output_size = self.data['output_size']
        self.all_words = self.data['all_words']
        self.tags = self.data['tags']
        self.model_state = self.data['model_state']

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

    # Function to respond to user input
    def respond(self, response, speak=True):
        print(f"{self.BOT_NAME}: {response}")
        if speak:
            self.engine.say(response)
            self.engine.runAndWait()

    # Function to generate a random response from an intent
    def generate_random_response(self, intent_tag):
        for intent in self.intents["intents"]:
            if intent_tag == intent["tag"]:
                return random.choice(intent['responses'])
        return None

    # Function to process user input
    def process_user_input(self, user_input):
        sentence = tokenize(user_input)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        return tag, prob

    # Function to extract the language from the input statement
    def extract_language(self, input_statement):
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
    def translate_and_speak(self, text, language_code):
        tts = gTTS(text=text, lang=language_code)
        tts.save("translated_text.mp3")
        playsound("translated_text.mp3")
        os.remove("translated_text.mp3")

    def handle_translation_request(self):
        user_text = input("You: ")
        response = f"The text you provided is: '{user_text}'. Is this correct?"
        self.respond(response)
        user_response = input("You: ")
        tag, prob = self.process_user_input(user_response)

        if tag == "yes" and prob.item() > 0.75:
            self.handle_detected_language(user_text)
        elif tag == "no" and prob.item() > 0.75:
            response = random.choice(self.IDK_RESPONSES)
            self.respond(response)

    def handle_detected_language(self, user_text):
        detected_language_code, detected_language_name = detect_language_full_name(user_text)
        response = f"The detected language is {detected_language_name}. Is this correct?"
        self.respond(response)
        user_response = input("You: ")
        tag, prob = self.process_user_input(user_response)

        if tag == "yes" and prob.item() > 0.75:
            self.handle_user_language_preference(user_text)
        elif tag == "no" and prob.item() > 0.75:
            self.respond("Sorry, I couldn't understand the language. Please rephrase your request.")

    def handle_user_language_preference(self,user_text):
        response = f"According to your language preferences, it's in {self.PREFERRED_LANGUAGE}. Do you want to continue with that?"
        self.respond(response)
        user_preference = input("You: ")
        tag, prob = self.process_user_input(user_preference)

        if tag == "yes" and prob.item() > 0.75:
            response = self.generate_random_response(tag)
            if response:
                self.respond(response)
                translated_text = translate_text(user_text, self.PREFERRED_LANGUAGE)
                self.display_and_speak_translated_text(translated_text, self.PREFERRED_LANGUAGE)
        elif tag == "no" and prob.item() > 0.75:
            self.handle_user_change_language(user_text)

    def handle_user_change_language(self,user_text):
        response = random.choice(self.CHANGE_IN_LANGUAGE_RESPONSES)
        self.respond(response)
        new_preference_lang = input("You: ")
        new_preference_lang = self.extract_language(new_preference_lang)
        response = f"Okay, you prefer to convert in {new_preference_lang} right?"
        self.respond(response)
        user_response = input("You: ")
        tag, prob = self.process_user_input(user_response)

        if tag == "yes" and prob.item() > 0.75:
            self.ask_to_set_default_language(new_preference_lang,user_text)
            translated_text = translate_text(user_text, new_preference_lang)
            self.display_and_speak_translated_text(translated_text, new_preference_lang)
        elif tag == "no" and prob.item() > 0.75:
            self.handle_user_change_language(user_text)
        else:
            self.respond("Okay, no translation will be performed.")

    def ask_to_set_default_language(self, new_preference_lang,user_text):
        response = f"Great, Would you like to make it the default preference?"
        self.respond(response)
        user_response = input("You: ")
        tag, prob = self.process_user_input(user_response)
        if tag == "yes" and prob.item() > 0.75:
            self.config["preferred_language"] = new_preference_lang
            with open('config.json', 'w') as file:
                json.dump(self.config, file, indent=2)
            response = f"Okay, I have set {new_preference_lang} as the default language preference."
            self.respond(response)
            translate_text(user_text, new_preference_lang)
        elif tag == "no" and prob.item() > 0.75:
            response = self.generate_random_response(tag)
            self.respond(response)
            translate_text(user_text, new_preference_lang)


    def display_and_speak_translated_text(self, translated_text, language_name):
        try:
            languageCodeDict = googletrans.LANGUAGES
            preferred_language_code = list(languageCodeDict.keys())[list(languageCodeDict.values()).index(self.PREFERRED_LANGUAGE.lower())]
        except KeyError:
            self.respond(random.choice(self.LANGUAGE_DETECT_ERROR_HANDLE))
            return

        self.respond(f"Here's what you were expecting: {translated_text}")
        self.translate_and_speak(translated_text, preferred_language_code)

    def handle_unrecognized_language(self,user_text):
        response = random.choice(self.REQUEST_FOR_LANGUAGE)
        self.respond(response)
        user_response = input("You: ")
        actual_lang = self.extract_language(user_response)
        response = f"Okay, you mean to convert it into {actual_lang} right?"
        self.respond(response)
        tag, prob = self.process_user_input(user_response)

        if tag == "yes" and prob.item() > 0.75:
            self.display_and_speak_translated_text(user_text, actual_lang)
        elif tag == "no" and prob.item() > 0.75:
            response = random.choice(self.IDK_RESPONSES)
            self.respond(response)

    def run_chat(self):
        print("Let's Chat!")

        while True:
            sentence = input("You: ")

            tag, prob = self.process_user_input(sentence)

            if prob.item() > 0.75:
                response = self.generate_random_response(tag)

                if response:
                    self.respond(response)

                    if tag == "goodbye":
                        quit()
                    elif tag == "translateRequest":
                        self.handle_translation_request()
            else:
                response = random.choice(self.IDK_RESPONSES)
                self.respond(response)

        # Shut down the pyttsx3 engine when done
        self.engine.stop()
        self.engine.runAndWait()

if __name__ == '__main__':
    chatbot = ChatBotSingleton()
    chatbot.run_chat()
