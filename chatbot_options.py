import speech_recognition as sr

def text_input():
    user_input = input("Enter your text response: ")
    return user_input

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print("You said: " + user_input)
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        user_input = None

    return user_input

while True:
    choice = input("Press 1 for text and 2 for voice (press 'q' to quit): ")

    if choice == '1':
        text_response = text_input()
        print("Text Response:", text_response)
    elif choice == '2':
        voice_response = voice_input()
        if voice_response:
            print("Voice Response:", voice_response)
    elif choice.lower() == 'q':
        break
    else:
        print("Invalid choice. Please press 1 for text or 2 for voice.")
