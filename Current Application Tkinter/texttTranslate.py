from langdetect import detect
from googletrans import Translator
from iso639 import languages

def detect_language_full_name(text):
    try:
        detected_language_code = detect(text)
        full_language_name = languages.get(part1=detected_language_code).name
        return detected_language_code, full_language_name
    except:
        return "undetermined", "Language detection failed"

def translate_text(text, target_language_code):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src='auto', dest=target_language_code)
        return translated_text.text
    except:
        return "Translation failed"