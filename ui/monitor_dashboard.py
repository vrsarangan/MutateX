import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import time
import os
import socket

from database import get_db

CARD_BG = "#0d0d0d"
CARD_BORDER = "#4caf50"
TEXT_COLOR = "#4caf50"
MAIN_BG = "#dce7d4"

def create_monitor_dashboard(parent):
    outer_frame = tk.Frame(parent, bg=MAIN_BG)
    outer_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer_frame, bg=MAIN_BG, highlightthickness=0)
    v_scroll = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)

    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canvas, bg=MAIN_BG)
    scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def resize_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(scrollable_window, width=event.width)

    scrollable_frame.bind("<Configure>", resize_scroll_region)
    canvas.bind("<Configure>", resize_scroll_region)

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

    # Cards
    cpu_card = create_card("CPU", 0, 0)
    mem_card = create_card("Memory", 0, 1)
    task_card = create_card("Task List", 0, 2)
    process_card = create_card("Process List", 1, 0)
    net_card = create_card("Network Traffic Monitor", 1, 1)
    js_card = create_card("Suspicious JavaScript Execution", 1, 2)
    host_card = create_card("Host Info", 2, 0)
    traffic_card = create_card("Network Summary", 2, 1)
    behavior_card = create_card("Behavior Anomaly Summary", 2, 2)

    # CPU Chart
    cpu_fig, cpu_ax = plt.subplots(figsize=(2, 2), facecolor=CARD_BG)
    cpu_canvas = FigureCanvasTkAgg(cpu_fig, master=cpu_card)
    cpu_canvas.get_tk_widget().pack(expand=True, fill="both")

    # Memory Chart
    mem_fig, mem_ax = plt.subplots(figsize=(2, 2), facecolor=CARD_BG)
    mem_canvas = FigureCanvasTkAgg(mem_fig, master=mem_card)
    mem_canvas.get_tk_widget().pack(expand=True, fill="both")

    # Task Listbox
    task_listbox = tk.Listbox(task_card, bg=CARD_BG, fg="white", selectbackground="#444")
    task_listbox.pack(expand=True, fill="both")

    # Process Listbox
    process_listbox = tk.Listbox(process_card, bg=CARD_BG, fg="white", selectbackground="#444")
    process_listbox.pack(expand=True, fill="both")

    # JavaScript Suspicion Listbox
    js_listbox = tk.Listbox(js_card, bg=CARD_BG, fg="white", selectbackground="#444")
    js_listbox.pack(expand=True, fill="both")

    # Network Table
    columns = ("Proto", "Source IP", "Dest IP", "Src Port", "Dst Port", "Packets")
    network_table = ttk.Treeview(net_card, columns=columns, show="headings")
    for col in columns:
        network_table.heading(col, text=col)
        network_table.column(col, width=100, anchor="center")
    network_table.pack(expand=True, fill="both")

    # Text areas
    host_text = tk.Text(host_card, height=5, bg=CARD_BG, fg="white", relief="flat")
    host_text.pack(fill="both", expand=True)

    traffic_text = tk.Text(traffic_card, height=5, bg=CARD_BG, fg="white", relief="flat")
    traffic_text.pack(fill="both", expand=True)

    behavior_text = tk.Text(behavior_card, height=5, bg=CARD_BG, fg="white", relief="flat")
    behavior_text.pack(fill="both", expand=True)
    behavior_text.insert(tk.END, "No anomalies detected.\nMonitoring...")

    # Treeview styling
    style = ttk.Style()
    style.configure("Treeview", background=CARD_BG, fieldbackground=CARD_BG,
                    foreground="white", rowheight=30, bordercolor=CARD_BORDER)
    style.map("Treeview", background=[('selected', '#333')])

    def update_data():
        db = get_db()
        while True:
            latest = db.system_metrics.find_one({"_id": "live"})
            if latest:
                cpu_percent = latest.get('cpu_percent', 0)
                mem = latest.get('memory', {})
                net = latest.get('net_io', {})
                hostname = latest.get("hostname", socket.gethostname())
                uptime_sec = latest.get("uptime", 0)
                boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - uptime_sec))

                # CPU Chart
                cpu_ax.clear()
                cpu_ax.pie(
                    [cpu_percent, 100 - cpu_percent],
                    labels=[f"Used {cpu_percent}%", f"Free {100 - cpu_percent}%"],
                    colors=["#4caf50", "#2e7d32"],
                    startangle=90,
                    wedgeprops={"edgecolor": "white"}
                )
                cpu_canvas.draw()

                # Memory Chart
                if mem:
                    used = mem.get("used", 0) / (1024 ** 3)
                    avail = mem.get("available", 0) / (1024 ** 3)
                    mem_ax.clear()
                    mem_ax.pie(
                        [used, avail],
                        labels=[f"Used {used:.1f}GB", f"Free {avail:.1f}GB"],
                        colors=["#81c784", "#388e3c"],
                        startangle=90,
                        wedgeprops={"edgecolor": "white"}
                    )
                    mem_canvas.draw()

                # Network Table
                network_table.delete(*network_table.get_children())
                for conn in latest.get('connections', [])[:10]:
                    network_table.insert("", "end", values=(
                        conn.get('proto', ''),
                        conn.get('src', ''),
                        conn.get('dst', ''),
                        conn.get('sport', ''),
                        conn.get('dport', ''),
                        conn.get('count', 0)
                    ))

                # Host Info
                host_text.delete("1.0", tk.END)
                host_text.insert(tk.END,
                    f"Hostname: {hostname}\nBoot Time: {boot_time}\nOS: {os.name}"
                )

                # Network Summary
                sent = net.get("bytes_sent", 0) / (1024 ** 2)
                recv = net.get("bytes_recv", 0) / (1024 ** 2)
                traffic_text.delete("1.0", tk.END)
                traffic_text.insert(tk.END,
                    f"Upload: {sent:.2f} MB\nDownload: {recv:.2f} MB"
                )

                # Process List
                processes = latest.get("processes", [])
                process_listbox.delete(0, tk.END)
                task_listbox.delete(0, tk.END)
                js_listbox.delete(0, tk.END)

                for proc in processes[:20]:
                    pid = proc.get("pid", "?")
                    name = proc.get("name", "Unknown")
                    cpu = proc.get("cpu_percent", 0)
                    memp = proc.get("memory_percent", 0)

                    process_listbox.insert(tk.END, f"{pid} {name} | CPU: {cpu:.1f}% | MEM: {memp:.1f}%")
                    task_listbox.insert(tk.END, name)

                    if "js" in name.lower() or "chrome" in name.lower():
                        js_listbox.insert(tk.END, f"{pid} {name}")

            time.sleep(2)

    threading.Thread(target=update_data, daemon=True).start()
    return outer_frame
