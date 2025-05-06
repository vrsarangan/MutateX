import tkinter as tk
from tkinter import ttk

def create_scan(content_frame):
    frame = tk.Frame(content_frame, bg="#0d0d0d")  # Dark background

    # Title
    tk.Label(frame, text="🧪 Configure Scan", font=("Segoe UI", 28, "bold"), fg="#76ff03", bg="#0d0d0d").place(x=150, y=50)

    # Duration input
    duration_frame = tk.Frame(frame, bg="#0d0d0d")
    duration_label = tk.Label(duration_frame, text="Scan Duration (sec):", font=("Segoe UI", 14), bg="#0d0d0d", fg="white")
    duration_entry = tk.Entry(duration_frame, width=10, font=("Segoe UI", 14), bg="#1f1f1f", fg="white", insertbackground="white")
    duration_label.pack(side=tk.LEFT, padx=5)
    duration_entry.pack(side=tk.LEFT, padx=5)
    duration_frame.place(x=150, y=130)

    # Scan Level dropdown
    level_frame = tk.Frame(frame, bg="#0d0d0d")
    level_label = tk.Label(level_frame, text="Scan Level:", font=("Segoe UI", 14), bg="#0d0d0d", fg="white")
    level_var = tk.StringVar(value="Quick")
    level_dropdown = ttk.Combobox(level_frame, textvariable=level_var,
                                   values=["Quick", "Deep", "Custom"],
                                   state="readonly", width=15, font=("Segoe UI", 14))
    level_dropdown.configure(background="#1f1f1f", foreground="white")
    level_label.pack(side=tk.LEFT, padx=5)
    level_dropdown.pack(side=tk.LEFT, padx=5)
    level_frame.place(x=150, y=190)

    # Custom ttk style for dark mode combobox
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox",
                    fieldbackground="#1f1f1f",
                    background="#1f1f1f",
                    foreground="white",
                    arrowcolor="#76ff03")
    
    # Scan Targets Checkbuttons
    type_frame = tk.LabelFrame(frame, text="Scan Targets", font=("Segoe UI", 14, "bold"),
                               bg="#0d0d0d", fg="#76ff03", bd=2, relief="ridge", padx=10, pady=10)
    file_var = tk.BooleanVar()
    root_var = tk.BooleanVar()
    bootloader_var = tk.BooleanVar()

    file_cb = tk.Checkbutton(type_frame, text="📄 File Scan", variable=file_var,
                             font=("Segoe UI", 13), bg="#0d0d0d", fg="white", activebackground="#1f1f1f", selectcolor="#1f1f1f", activeforeground="#76ff03")
    root_cb = tk.Checkbutton(type_frame, text="🛡️ Root-Level Scan", variable=root_var,
                             font=("Segoe UI", 13), bg="#0d0d0d", fg="white", activebackground="#1f1f1f", selectcolor="#1f1f1f", activeforeground="#76ff03")
    bootloader_cb = tk.Checkbutton(type_frame, text="💾 Bootloader Scan", variable=bootloader_var,
                                   font=("Segoe UI", 13), bg="#0d0d0d", fg="white", activebackground="#1f1f1f", selectcolor="#1f1f1f", activeforeground="#76ff03")

    file_cb.pack(anchor="w", pady=2)
    root_cb.pack(anchor="w", pady=2)
    bootloader_cb.pack(anchor="w", pady=2)
    type_frame.place(x=150, y=260)

    # Start Scan Button
    def start_scan():
        duration = duration_entry.get()
        level = level_var.get()
        scan_targets = {
            "File Scan": file_var.get(),
            "Root-Level Scan": root_var.get(),
            "Bootloader Scan": bootloader_var.get()
        }
        print("Scan Configuration:")
        print(f"Duration: {duration}")
        print(f"Level: {level}")
        print(f"Targets: {scan_targets}")
        # Placeholder for scan logic

    tk.Button(frame, text="🚀 Start Scan", bg="#76ff03", fg="#0d0d0d",
              font=("Segoe UI", 16, "bold"), command=start_scan,
              activebackground="#64dd17", activeforeground="black").place(x=150, y=450, width=400, height=50)

    return frame
