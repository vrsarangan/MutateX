import tkinter as tk
from tkinter import ttk

def create_search(parent):
    search_frame = tk.Frame(parent, bg="#0d0d0d")

    # --- Search Input --- #
    search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), bg="#1a1a1a", fg="white",
                            insertbackground="white", relief="flat")
    search_entry.place(relx=0.5, y=30, anchor="center", width=350, height=30)
    search_entry.insert(0, "Search type of keywords")

    search_icon = tk.Label(search_frame, text="🔍", bg="#1a1a1a", fg="white", font=("Arial", 12))
    search_icon.place(relx=0.73, y=30, anchor="center")

    # --- Table Container --- #
    table_container = tk.Frame(search_frame, bg="#dbe7d2", bd=0)
    table_container.place(relx=0.5, rely=0.15, anchor="n", width=920, height=600)

    # --- Filters --- #
    type_options = ["Any", "Malware", "Trojan", "Worm", "Spyware", "Adware", "Rootkit"]
    severity_options = ["Any", "Critical", "Moderate", "Low", "Safe", "Unknown"]
    affected_options = ["Any", "Files", "Registry", "Memory", "Network", "Boot Sector"]

    # --- Create filter dropdowns --- #
    type_var = tk.StringVar(value="Any")
    date_var = tk.StringVar()
    severity_var = tk.StringVar(value="Any")
    affected_var = tk.StringVar(value="Any")

    filters = [
        ("Type", type_options, type_var),
        ("Date", None, date_var),  # Date entry
        ("Severity", severity_options, severity_var),
        ("Affected", affected_options, affected_var)
    ]

    for idx, (title, options, var) in enumerate(filters):
        filter_frame = tk.Frame(table_container, bg="#dbe7d2", width=200, height=80)
        filter_frame.place(x=20 + idx*220, y=20)
        filter_frame.pack_propagate(False)

        label = tk.Label(filter_frame, text=title, bg="#dbe7d2", fg="#4caf50",
                         font=("Segoe UI", 12, "bold"))
        label.pack(anchor="center")

        if options:
            combo = ttk.Combobox(filter_frame, textvariable=var, values=options, state="readonly")
            combo.pack(pady=5)
        else:
            entry = tk.Entry(filter_frame, textvariable=var, bg="white", relief="solid")
            entry.pack(pady=5)

    # --- Main Results Display --- #
    results_frame = tk.Frame(table_container, bg="#000000", width=880, height=400)
    results_frame.place(x=20, y=130)
    results_frame.pack_propagate(False)

    result_label = tk.Label(results_frame, text="Results will appear here...", bg="#000000",
                            fg="white", font=("Segoe UI", 12))
    result_label.pack(expand=True)

    return search_frame
