import googletrans
import speech_recognition as sr
import gtts
import playsound
import keyboard

input_lang = "en"
output_lang = "ml"

recognizer = sr.Recognizer()

def result():
    translator = googletrans.Translator()
    translation = translator.translate(text, dest=output_lang)
    print(translation.text)
    converted_audio = gtts.gTTS(translation.text, lang=output_lang)
    converted_audio.save("hello.mp3")
    playsound.playsound("hello.mp3")
    
with sr.Microphone() as source:
    print("Speak now... Press Enter to stop recording")
    recognizer.adjust_for_ambient_noise(source)

    try:
        voice = recognizer.listen(source, timeout=60)  # Set a timeout (e.g., 10 seconds)
        text = recognizer.recognize_google(voice, language=input_lang)
        print(text)
    except sr.WaitTimeoutError:
        print("Recording timed out.")

    try:
        # Implement a way to stop recording when Enter is pressed or Ctrl+C (keyboard interrupt)
        while True:
            if keyboard.is_pressed("enter"):
                result()  # Call the result function before breaking the loop
                break  # Exit the loop when Enter key is pressed
    except KeyboardInterrupt:
        pass  # Handle the keyboard interrupt (Ctrl+C)


#print(googletrans.LANGUAGES)

