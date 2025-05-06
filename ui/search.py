import tkinter as tk
from tkinter import ttk

def create_search(parent):
    def on_entry_click(event):
        if search_entry.get() == "Search type of keywords":
            search_entry.delete(0, "end")
            search_entry.config(fg="white")

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "Search type of keywords")
            search_entry.config(fg="grey")

    search_frame = tk.Frame(parent, bg="#0d0d0d")

    # --- Search Input --- #
    search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), bg="#1a1a1a",
                            fg="grey", insertbackground="white", relief="flat")
    search_entry.insert(0, "Search type of keywords")
    search_entry.bind("<FocusIn>", on_entry_click)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.place(relx=0.5, y=30, anchor="center", width=350, height=30)

    search_button = tk.Button(search_frame, text="Search", bg="#4caf50", fg="white",
                              font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
    search_button.place(relx=0.85, y=30, anchor="center", width=80, height=30)

    # --- Table Container --- #
    table_container = tk.Frame(search_frame, bg="#dbe7d2")
    table_container.place(relx=0.5, rely=0.15, anchor="n", width=920, height=600)

    # --- Filter Options --- #
    type_options = ["Any", "Malware", "Trojan", "Worm", "Spyware", "Adware", "Rootkit"]
    severity_options = ["Any", "Critical", "Moderate", "Low", "Safe", "Unknown"]
    affected_options = ["Any", "Files", "Registry", "Memory", "Network", "Boot Sector"]

    type_var = tk.StringVar(value="Any")
    date_var = tk.StringVar()
    severity_var = tk.StringVar(value="Any")
    affected_var = tk.StringVar(value="Any")

    filters = [
        ("Type", type_options, type_var),
        ("Date", None, date_var),
        ("Severity", severity_options, severity_var),
        ("Affected", affected_options, affected_var)
    ]

    # --- Filters UI --- #
    filter_frame = tk.Frame(table_container, bg="#dbe7d2")
    filter_frame.place(x=20, y=20)

    for i, (label_text, options, var) in enumerate(filters):
        frame = tk.Frame(filter_frame, bg="#dbe7d2")
        frame.grid(row=0, column=i, padx=15)

        label = tk.Label(frame, text=label_text, bg="#dbe7d2", fg="#4caf50",
                         font=("Segoe UI", 12, "bold"))
        label.pack(anchor="w")

        if options:
            combo = ttk.Combobox(frame, textvariable=var, values=options, state="readonly")
            combo.pack(pady=5)
        else:
            entry = tk.Entry(frame, textvariable=var, bg="white", relief="solid")
            entry.pack(pady=5)

    # --- Results Frame --- #
    results_frame = tk.Frame(table_container, bg="#000000", width=880, height=400)
    results_frame.place(x=20, y=100)
    results_frame.pack_propagate(False)

    result_label = tk.Label(results_frame, text="Results will appear here...", bg="#000000",
                            fg="white", font=("Segoe UI", 12))
    result_label.pack(expand=True)

    return search_frame
