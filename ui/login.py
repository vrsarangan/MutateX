import tkinter as tk
from tkinter import messagebox

def create_login_page(content_frame, login_callback):
    frame = tk.Frame(content_frame, bg="#121212")

    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    clear_frame()

    tk.Label(frame, text="Login", font=("Segoe UI", 32, "bold"), fg="#4caf50", bg="#121212").pack(pady=50)

    tk.Label(frame, text="Email:", font=("Arial", 18), fg="white", bg="#121212").pack(pady=10)
    email_entry = tk.Entry(frame, font=("Arial", 14), bg="#333333", fg="white", bd=0, relief="flat")
    email_entry.pack(pady=10, padx=20, fill="x")

    tk.Label(frame, text="Password:", font=("Arial", 18), fg="white", bg="#121212").pack(pady=10)
    password_entry = tk.Entry(frame, font=("Arial", 14), bg="#333333", fg="white", bd=0, relief="flat", show="*")
    password_entry.pack(pady=10, padx=20, fill="x")

    def on_login_click():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password:
            messagebox.showerror("Input Error", "Please enter both email and password.")
            return
        login_callback(email, password)

    login_button = tk.Button(frame, text="Login", font=("Segoe UI", 16), bg="#4caf50", fg="white", relief="flat", command=on_login_click)
    login_button.pack(pady=20)

    return frame
