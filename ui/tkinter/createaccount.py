import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.setup_login_ui()

    def setup_login_ui(self):
        # Create and place labels and entry fields for User ID and Password
        self.user_label = tk.Label(self.root, text="User ID:")
        self.user_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        # Create and place the Submit button
        self.login_button = tk.Button(self.root, text="Submit", command=self.login)
        self.login_button.pack()

        # Create and place buttons for creating an account and resetting password
        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.show_create_account)
        self.create_account_button.pack()

        self.forget_password_button = tk.Button(self.root, text="Forget User ID/Password", command=self.forget_password)
        self.forget_password_button.pack()

    def show_create_account(self):
        # Clear the login UI
        self.user_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_button.pack_forget()
        self.create_account_button.pack_forget()
        self.forget_password_button.pack_forget()

        # Create account UI elements
        self.create_account_label = tk.Label(self.root, text="Create Account")
        self.create_account_label.pack()

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.confirm_password_label = tk.Label(self.root, text="Confirm Password:")
        self.confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack()

        self.dob_label = tk.Label(self.root, text="Date of Birth:")
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.root)
        self.dob_entry.pack()

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        self.recovery_question_label = tk.Label(self.root, text="Recovery Question:")
        self.recovery_question_label.pack()
        recovery_questions = [
            "What is your favorite food?",
            "What is your favorite book?",
            "What is your favorite sports?",
            "What is your favorite place?"
        ]
        self.recovery_question_var = tk.StringVar(self.root)
        self.recovery_question_dropdown = ttk.Combobox(self.root, textvariable=self.recovery_question_var, values=recovery_questions)
        self.recovery_question_dropdown.pack()

        self.recovery_answer_label = tk.Label(self.root, text="Recovery Answer:")
        self.recovery_answer_label.pack()
        self.recovery_answer_entry = tk.Entry(self.root)
        self.recovery_answer_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_account)
        self.submit_button.pack()

        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_login)
        self.back_button.pack()

    def back_to_login(self):
        # Clear the create account UI
        self.create_account_label.pack_forget()
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.confirm_password_label.pack_forget()
        self.confirm_password_entry.pack_forget()
        self.dob_label.pack_forget()
        self.dob_entry.pack_forget()
        self.email_label.pack_forget()
        self.email_entry.pack_forget()
        self.recovery_question_label.pack_forget()
        self.recovery_question_dropdown.pack_forget()
        self.recovery_answer_label.pack_forget()
        self.recovery_answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.back_button.pack_forget()

        # Restore the login UI
        self.setup_login_ui()

    def submit_account(self):
        # Get values from the create account form
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        dob = self.dob_entry.get()
        email = self.email_entry.get()
        recovery_question = self.recovery_question_var.get()
        recovery_answer = self.recovery_answer_entry.get()

        # Validate email format using regular expression
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        # Validate password and confirm password match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Add your logic to store the user account information here
        # For this example, we'll just show the collected information
        messagebox.showinfo("Account Created", f"Account created for User: {username}\nDOB: {dob}\nEmail: {email}\nRecovery Question: {recovery_question}\nRecovery Answer: {recovery_answer}")

    def login(self):
        user = self.username_entry.get()
        password = self.password_entry.get()

        # Here, you can add your logic to validate the user's credentials
        # For this example, we will just show a message box
        messagebox.showinfo("Login", f"Logged in with User: {user} and Password: {password}")

    def forget_password(self):
        # Add logic for handling forgotten passwords or user IDs
        messagebox.showinfo("Forget Password", "Forgot password or User ID")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
