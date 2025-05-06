import tkinter as tk
from tkinter import ttk

def create_history(parent):
    frame = tk.Frame(parent, bg="#0d0d0d")

    # Title Label
    tk.Label(frame, text="📜 Scan History", font=("Courier", 32, "bold"),
             bg="#0d0d0d", fg="#4caf50").pack(pady=20)

    # Style the Treeview to match dark theme
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#1a1a1a",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#1a1a1a",
                    bordercolor="#4caf50",
                    borderwidth=1)
    style.map("Treeview",
              background=[("selected", "#4caf50")],
              foreground=[("selected", "#0d0d0d")])

    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    background="#2e2e2e",
                    foreground="#4caf50")

    # Treeview setup
    columns = ("scan_id", "date", "filename", "status")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    tree.pack(padx=20, pady=20, fill="both", expand=True)

    # Headings
    tree.heading("scan_id", text="Scan ID")
    tree.heading("date", text="Date")
    tree.heading("filename", text="Filename")
    tree.heading("status", text="Status")

    # Column layout
    tree.column("scan_id", width=100, anchor="center")
    tree.column("date", width=150, anchor="center")
    tree.column("filename", width=300, anchor="w")
    tree.column("status", width=150, anchor="center")

    # Sample data
    sample_data = [
        (1, "2025-04-26", "malware_sample.exe", "Quarantined"),
        (2, "2025-04-25", "good_file.txt", "Safe"),
        (3, "2025-04-24", "suspicious_script.js", "Flagged"),
    ]

    for item in sample_data:
        tree.insert('', 'end', values=item)

    return frame
