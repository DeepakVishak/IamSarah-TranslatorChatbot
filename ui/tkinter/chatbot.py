import tkinter as tk
import threading
import speech_recognition as sr

class SpeechRecognitionChatbot:
    def __init__(self, master):
        self.master = master
        master.title("Speech Recognition Chatbot")

        # Create a text widget to display the chat
        self.chat_display = tk.Text(master, height=15, width=40)
        self.chat_display.pack(padx=10, pady=10)

        # Create a Text widget for user input with word wrap
        self.user_input = tk.Text(master, height=4, width=40, wrap=tk.WORD)
        self.user_input.pack(padx=10, pady=10)
        
        # Create a button to trigger speech recognition
        self.send_button = tk.Button(master, text="Speech", command=self.on_button_click)
        self.send_button.pack(pady=10)

        # Bind key press event to update button text
        self.user_input.bind("<KeyRelease>", lambda event: self.update_button_text())

        # Flag to indicate if speech recognition is in progress
        self.listening = False

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                self.listening = True
                self.update_button_text()
                audio_data = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio_data)
                self.user_input.delete(1.0, tk.END)
                self.user_input.insert(tk.END, text)
                self.update_button_text()
            except sr.UnknownValueError:
                self.display_message("Bot: Speech not recognized")
            except sr.RequestError as e:
                self.display_message(f"Bot: Error with the speech recognition service: {e}")
            finally:
                self.listening = False
                self.update_button_text()

    def send_message(self):
        user_message = self.user_input.get(1.0, tk.END).strip()
        if user_message:
            self.display_message("You: " + user_message)

            # Simple echo mechanism (replace with actual chatbot logic)
            bot_response = f"Bot: You said: {user_message}"
            self.display_message(bot_response)

            # Clear the user input
            self.user_input.delete(1.0, tk.END)
            self.update_button_text()

    def on_button_click(self):
        # Determine whether to call send_message or recognize_speech
        if self.listening:
            return  # If already listening, do nothing
        if self.send_button.cget("text") == "Send":
            self.send_message()
        else:
            threading.Thread(target=self.recognize_speech).start()

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)

    def update_button_text(self):
        # Update button text dynamically based on user_input and listening state
        if self.listening:
            button_text = "Listening"
        else:
            button_text = "Send" if self.user_input.get(1.0, tk.END).strip() else "Speech"
        self.send_button.config(text=button_text)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = SpeechRecognitionChatbot(root)
    root.mainloop()
