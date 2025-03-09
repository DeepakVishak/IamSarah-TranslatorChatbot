import speech_recognition as sr
import threading
import time

text_input = None
speech_input = None

def text_thread():
    global text_input
    text_input = input("Enter the input")
    if not text_input:
        text_input = None

def speech_thread():
    global speech_input
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Listening... (Press Enter to stop)")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)
                print("Recording...")
                try:
                    text = recognizer.recognize_google(audio)
                    speech_input = text
                    print("You said: " + speech_input)
                except sr.UnknownValueError:
                    pass  # Ignore errors if speech not recognized
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    text_thread = threading.Thread(target=text_thread)
    speech_thread = threading.Thread(target=speech_thread)

    text_thread.start()
    speech_thread.start()

    text_thread.join()
    speech_thread.join()

    # Use the condition you mentioned to select the appropriate input
    if text_input:
        user_input = text_input
    else:
        user_input = speech_input

    print("User input:", user_input)
