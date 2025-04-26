import tkinter as tk
from tkinter import ttk

def create_history(parent):
    frame = tk.Frame(parent, bg="#ffffff")

    tk.Label(frame, text="📜 Scan History", font=("Arial", 32, "bold"), bg="#ffffff", fg="#333333").pack(pady=20)

    columns = ("scan_id", "date", "filename", "status")

    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    tree.pack(padx=20, pady=20, fill="both", expand=True)

    # Define headings
    tree.heading("scan_id", text="Scan ID")
    tree.heading("date", text="Date")
    tree.heading("filename", text="Filename")
    tree.heading("status", text="Status")

    # Define column widths
    tree.column("scan_id", width=100, anchor="center")
    tree.column("date", width=150, anchor="center")
    tree.column("filename", width=300, anchor="w")
    tree.column("status", width=100, anchor="center")

    # Dummy sample data
    sample_data = [
        (1, "2025-04-26", "malware_sample.exe", "Quarantined"),
        (2, "2025-04-25", "good_file.txt", "Safe"),
        (3, "2025-04-24", "suspicious_script.js", "Flagged"),
    ]

    for item in sample_data:
        tree.insert('', 'end', values=item)

    return frame
