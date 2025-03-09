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

if __name__ == "__main__":
    text = input("Enter text: ")
    
    # Detect the language and get its full name
    detected_language_code, detected_language_name = detect_language_full_name(text)
    
    if detected_language_code == "undetermined":
        print("Language detection failed (undetermined)")
    else:
        print(f"Detected language: {detected_language_name}")
    
    target_language = input("Enter target language (e.g., Malayalam): ")
    
    if not target_language:
        target_language_code = "en"  # Default to English
    else:
        target_language_code = target_language
    
    translated_text = translate_text(text, target_language_code)
    print(f"Translated to {target_language_code}: {translated_text}")
