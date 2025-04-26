import tkinter as tk
from ui.sidebar import create_sidebar
from ui.dashboard import create_dashboard
from ui.monitor_dashboard import create_monitor_dashboard
from ui.history import create_history
from ui.settings import create_settings
from ui.scan import create_scan
from ui.search import create_search

# ---------------- Window Setup ---------------- #
root = tk.Tk()
root.title("Mutated Malware Detector")
root.geometry("1200x800")
root.configure(bg="#0d0d0d")

# ---------------- Frame Management ---------------- #
content_frame = tk.Frame(root, bg="#0d0d0d")
content_frame.place(x=60, y=0, relwidth=1, relheight=1, anchor="nw")

frames = {}

# ---------------- Show Frame Function ---------------- #
def show_frame(name):
    for frame in frames.values():
        frame.place_forget()
    frames[name].place(relwidth=1, relheight=1)

# ---------------- Create Sidebar ---------------- #
sidebar = create_sidebar(root, content_frame, frames, show_frame)

# ---------------- Create Pages ---------------- #
frames["Dashboard"] = create_dashboard(content_frame)
frames["Monitor"] = create_monitor_dashboard(content_frame)
frames["History"] = create_history(content_frame)
frames["Settings"] = create_settings(content_frame)
frames["Scan"] = create_scan(content_frame)
frames["Search"] = create_search(content_frame)

# ---------------- Default View ---------------- #
show_frame("Dashboard")

# ---------------- Start App ---------------- #
root.mainloop()
