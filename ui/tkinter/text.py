import tkinter as tk
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio_data = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio_data)
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, text)
        except sr.UnknownValueError:
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, "Speech not recognized")
        except sr.RequestError as e:
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, f"Error with the speech recognition service: {e}")

# Create the main window
root = tk.Tk()
root.title("Speech Recognition")

# Create a button to trigger speech recognition
speech_button = tk.Button(root, text="Speech", command=recognize_speech)
speech_button.pack(pady=10)

# Create a text widget to display the recognized speech
text_output = tk.Text(root, height=5, width=40)
text_output.pack(padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
