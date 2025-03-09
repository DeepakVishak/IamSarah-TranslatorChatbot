import tkinter as tk
from threading import Thread
from chatbot import ChatBotSingleton  # Assuming the provided code is in a file named 'chatbot.py'

class TkinterChatBotApp:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter Chatbot")

        # Create a text widget to display the chat
        self.chat_display = tk.Text(master, height=15, width=40)
        self.chat_display.pack(padx=10, pady=10)

        # Create a Text widget for user input with word wrap
        self.user_input = tk.Text(master, height=4, width=40, wrap=tk.WORD)
        self.user_input.pack(padx=10, pady=10)

        # Create a button to send the user input to the chatbot
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        # Initialize the chatbot
        self.chatbot = ChatBotSingleton()

    def send_message(self):
        user_message = self.user_input.get(1.0, tk.END).strip()
        if user_message:
            # Display user's message in the chat
            self.display_message("You: " + user_message)

            # Process the user's message in a separate thread
            Thread(target=self.process_user_message, args=(user_message,)).start()

            # Clear the user input
            self.user_input.delete(1.0, tk.END)

    def process_user_message(self, user_message):
        # Send the user's message to the chatbot and get the response
        response = self.chatbot.process_user_input(user_message)

        # Display the chatbot's response in the chat
        self.display_message(response)

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TkinterChatBotApp(root)
    root.mainloop()
