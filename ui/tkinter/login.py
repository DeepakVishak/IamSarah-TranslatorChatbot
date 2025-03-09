import tkinter as tk
from tkinter import messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Create and place labels and entry fields for User ID and Password
        self.user_label = tk.Label(root, text="User ID:")
        self.user_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")  # Show * for password input
        self.password_entry.pack()

        # Create and place the Submit button
        self.login_button = tk.Button(root, text="Submit", command=self.login)
        self.login_button.pack()

        # Create and place buttons for creating an account and resetting password
        self.create_account_button = tk.Button(root, text="Create Account", command=self.create_account)
        self.create_account_button.pack()

        self.forget_password_button = tk.Button(root, text="Forget User ID/Password", command=self.forget_password)
        self.forget_password_button.pack()

    def login(self):
        user = self.username_entry.get()
        password = self.password_entry.get()

        # Here, you can add your logic to validate the user's credentials
        # For this example, we will just show a message box
        messagebox.showinfo("Login", f"Logged in with User: {user} and Password: {password}")

    def create_account(self):
        # Add logic to create a new user account
        messagebox.showinfo("Create Account", "Create an account")

    def forget_password(self):
        # Add logic for handling forgotten passwords or user IDs
        messagebox.showinfo("Forget Password", "Forgot password or User ID")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
