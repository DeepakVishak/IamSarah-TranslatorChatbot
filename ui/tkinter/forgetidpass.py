import tkinter as tk
from tkinter import messagebox

def switch_recovery_option():
    if recovery_option.get() == 1:
        # Show fields for recovering username
        dob_label.pack()
        dob_entry.pack()
        recovery_question_label.config(text="What's your favorite food?")
        recovery_question_label.pack()
        recovery_answer_entry.pack()
        otp_entry.pack_forget()
        confirm_button.pack_forget()
        new_password_label.pack_forget()
        confirm_new_password_label.pack_forget()
        new_password_entry.pack_forget()
        confirm_new_password_entry.pack_forget()
        submit_button.pack()
    else:
        # Show fields for recovering password
        dob_label.pack_forget()
        dob_entry.pack_forget()
        recovery_question_label.config(text="What's your favorite food?")
        recovery_question_label.pack()
        recovery_answer_entry.pack()
        otp_entry.pack()
        confirm_button.pack()
        new_password_label.pack_forget()
        confirm_new_password_label.pack_forget()
        new_password_entry.pack_forget()
        confirm_new_password_entry.pack_forget()
        submit_button.pack()

def submit():
    if recovery_option.get() == 1:
        # Logic to recover username
        # You can implement this logic here
        messagebox.showinfo("Username Recovery", "Username has been sent to your email.")
    else:
        # Logic to recover password
        # You can implement this logic here, including OTP validation and password change
        if otp_entry.get() == "12345":
            new_password_label.pack()
            confirm_new_password_label.pack()
            new_password_entry.pack()
            confirm_new_password_entry.pack()
            submit_button.config(command=change_password)
        else:
            messagebox.showerror("Invalid OTP", "Please enter a valid OTP.")

def change_password():
    # Logic to change the password
    # You can implement this logic here
    messagebox.showinfo("Password Changed", "Your password has been changed.")
    switch_recovery_option()

# Create the main window
root = tk.Tk()
root.title("Password/Username Recovery")

# Create radio buttons for recovery options
recovery_option = tk.IntVar()
username_radio = tk.Radiobutton(root, text="Recover Username", variable=recovery_option, value=1, command=switch_recovery_option)
password_radio = tk.Radiobutton(root, text="Recover Password", variable=recovery_option, value=2, command=switch_recovery_option)
username_radio.pack()
password_radio.pack()
username_radio.select()  # Set the default option

# Create and place the common fields
recovery_question_label = tk.Label(root, text="What's your favorite food?")
recovery_question_label.pack()
recovery_answer_entry = tk.Entry(root)
recovery_answer_entry.pack()

# Fields for recovering username
dob_label = tk.Label(root, text="Date of Birth:")
dob_entry = tk.Entry(root)
dob_label.pack()
dob_entry.pack()

# Fields for recovering password
otp_label = tk.Label(root, text="Enter OTP:")
otp_entry = tk.Entry(root)
otp_label.pack()
otp_entry.pack()

# Fields for changing the password
new_password_label = tk.Label(root, text="New Password:")
new_password_entry = tk.Entry(root, show="*")
confirm_new_password_label = tk.Label(root, text="Confirm New Password:")
confirm_new_password_entry = tk.Entry(root, show="*")

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Create the main loop
root.mainloop()
