# ui/scan.py

import tkinter as tk

def create_scan(content_frame):
    frame = tk.Frame(content_frame, bg="#f0f0f0")
    label = tk.Label(frame, text="🧪 Start a New Scan", font=("Arial", 24), bg="#f0f0f0")
    label.pack(pady=100)
    return frame
