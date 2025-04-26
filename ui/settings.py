import tkinter as tk

def create_settings(parent):
    # --- Main Settings Frame --- #
    settings_frame = tk.Frame(parent, bg="#0d0d0d")

    # Left Sidebar Panel
    sidebar = tk.Frame(settings_frame, bg="#dbe7d2", width=300, height=700)
    sidebar.pack(side="left", fill="y", padx=20, pady=20)
    sidebar.pack_propagate(False)

    # Right Content Panel
    content_panel = tk.Frame(settings_frame, bg="#000000", width=800, height=700)
    content_panel.pack(side="left", expand=True, fill="both", padx=(0, 20), pady=20)
    content_panel.pack_propagate(False)

    # Dummy content label
    default_label = tk.Label(content_panel, text="Select a setting on the left", font=("Segoe UI", 18), fg="white", bg="#000000")
    default_label.pack(expand=True)

    # Sections for settings
    sections = [
        "General",
        "Scan",
        "Real-time Monitoring",
        "Sandbox",
        "Threat intelligence integration",
        "Logging & Report",
        "Security & Privacy",
        "Advanced"
    ]

    buttons = []

    # Highlight function
    def select_section(name):
        for btn in buttons:
            btn.config(bg="#1f1f1f", fg="#76ff03")

        for btn in buttons:
            if btn.cget("text") == name:
                btn.config(bg="#333333", fg="white")

        default_label.config(text=f"{name} Settings")

    # Create section buttons
    for section in sections:
        btn = tk.Button(
            sidebar,
            text=section,
            font=("Segoe UI", 12, "bold"),
            bg="#1f1f1f",
            fg="#76ff03",
            relief="flat",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=8,
            anchor="w",
            command=lambda name=section: select_section(name)
        )
        btn.pack(fill="x", pady=8, padx=15)
        buttons.append(btn)

    # Select the first one by default
    select_section("General")

    return settings_frame
