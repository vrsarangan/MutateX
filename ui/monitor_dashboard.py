# ui/monitor_dashboard.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import time
from database import get_db

CARD_BG = "#0d0d0d"
CARD_BORDER = "#4caf50"
TEXT_COLOR = "#4caf50"
MAIN_BG = "#dce7d4"

def create_monitor_dashboard(parent):
    outer_frame = tk.Frame(parent, bg=MAIN_BG)
    outer_frame.pack(fill="both", expand=True)

    # Canvas and Scrollbar
    canvas = tk.Canvas(outer_frame, bg=MAIN_BG, highlightthickness=0)
    v_scroll = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)

    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollable frame inside the canvas
    scrollable_frame = tk.Frame(canvas, bg=MAIN_BG)
    scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def resize_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Resize the window width to match the canvas width
        canvas.itemconfig(scrollable_window, width=event.width)

    scrollable_frame.bind("<Configure>", resize_scroll_region)
    canvas.bind("<Configure>", resize_scroll_region)

    # Make outer columns flexible
    for col in range(3):
        scrollable_frame.grid_columnconfigure(col, weight=1, uniform="col")

    card_widgets = {}

    def create_card(title, row, col, rowspan=1, colspan=1):
        card = tk.Frame(scrollable_frame, bg=CARD_BG, bd=2, relief="solid",
                        highlightbackground=CARD_BORDER, highlightthickness=1)
        card.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                  padx=15, pady=15, sticky="nsew")

        title_lbl = tk.Label(card, text=title, font=("Arial", 12, "bold"),
                             fg=TEXT_COLOR, bg=CARD_BG)
        title_lbl.pack(anchor="w", padx=10, pady=(10, 0))

        content = tk.Frame(card, bg=CARD_BG)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        card_widgets[title] = content
        return content

    # Create Cards
    cpu_card = create_card("CPU", 0, 0)
    mem_card = create_card("Memory", 0, 1)
    create_card("Task List", 0, 2)

    create_card("Process List", 1, 0)
    net_card = create_card("Network Traffic Monitor", 1, 1)
    create_card("Suspicious JavaScript Execution", 1, 2)

    create_card("Registry Changes", 2, 0)
    create_card("Behavior Analysis", 2, 1)
    create_card("+", 2, 2)

    # CPU Chart
    cpu_fig, cpu_ax = plt.subplots(figsize=(2, 2), facecolor=CARD_BG)
    cpu_canvas = FigureCanvasTkAgg(cpu_fig, master=cpu_card)
    cpu_canvas.get_tk_widget().pack(expand=True, fill="both")

    # Memory Chart
    mem_fig, mem_ax = plt.subplots(figsize=(2, 2), facecolor=CARD_BG)
    mem_canvas = FigureCanvasTkAgg(mem_fig, master=mem_card)
    mem_canvas.get_tk_widget().pack(expand=True, fill="both")

    # Network Table
    columns = ("Proto", "Source IP", "Dest IP", "Src Port", "Dst Port", "Packets")
    network_table = ttk.Treeview(net_card, columns=columns, show="headings")
    for col in columns:
        network_table.heading(col, text=col)
        network_table.column(col, width=100, anchor="center")
    network_table.pack(expand=True, fill="both")

    style = ttk.Style()
    style.configure("Treeview", background=CARD_BG, fieldbackground=CARD_BG,
                    foreground="white", rowheight=30, bordercolor=CARD_BORDER)
    style.map("Treeview", background=[('selected', '#333')])

    # Update Data Thread
    def update_data():
        db = get_db()
        while True:
            latest = db.system_metrics.find_one({"_id": "live"})
            if latest:
                cpu_percent = latest.get('cpu_percent', 0)
                mem = latest.get('memory', {})

                # Update CPU Chart
                cpu_ax.clear()
                cpu_ax.pie(
                    [cpu_percent, 100-cpu_percent],
                    labels=[f"Used {cpu_percent}%", f"Free {100-cpu_percent}%"],
                    colors=["#4caf50", "#2e7d32"],
                    startangle=90,
                    wedgeprops={"edgecolor": "white"}
                )
                cpu_canvas.draw()

                # Update Memory Chart
                if mem:
                    used = mem.get("used", 0) / (1024**3)
                    avail = mem.get("available", 0) / (1024**3)
                    mem_ax.clear()
                    mem_ax.pie(
                        [used, avail],
                        labels=[f"Used {used:.1f}GB", f"Free {avail:.1f}GB"],
                        colors=["#81c784", "#388e3c"],
                        startangle=90,
                        wedgeprops={"edgecolor": "white"}
                    )
                    mem_canvas.draw()

                # Update Network Table
                network_table.delete(*network_table.get_children())
                connections = latest.get('connections', [])[:10]
                for conn in connections:
                    proto = conn.get('proto', '')
                    src = conn.get('src', '')
                    dst = conn.get('dst', '')
                    sport = conn.get('sport', '')
                    dport = conn.get('dport', '')
                    packets = conn.get('count', 0)
                    network_table.insert("", "end", values=(proto, src, dst, sport, dport, packets))

            time.sleep(2)

    threading.Thread(target=update_data, daemon=True).start()

    return outer_frame
