import tkinter as tk
from ui.sidebar import create_sidebar
from ui.dashboard import create_dashboard
from ui.monitor_dashboard import create_monitor_dashboard
from ui.history import create_history
from ui.settings import create_settings
from ui.scan import create_scan
from ui.search import create_search
from ui.code_analysis import create_code_analysis
from ui.quarantine import create_quarantine
from ui.userprofile import create_user_profile
from ui.notification import create_notification
from ui.ml import create_ml_page

from dotenv import load_dotenv
from pymongo import MongoClient
import os

user = {
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'role': 'Admin',
    'privilege': 'High',
    'phone': '1234567890',
    'department': 'IT',
    'last_login': '2025-05-01 10:00:00',
    'created_at': '2024-01-01 08:00:00'
}

# ---------------- Environment & MongoDB Setup ---------------- #
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client.mutatex
users_collection = db.users

# ---------------- Main Window Setup ---------------- #
root = tk.Tk()
root.title("Mutated Malware Detector")
root.geometry("1200x800")
root.configure(bg="#0d0d0d")

# ---------------- Frame Management ---------------- #
content_frame = tk.Frame(root, bg="#0d0d0d")
content_frame.place(x=60, y=0, relwidth=1.0 - 60/1200, relheight=1, anchor="nw")

frames = {}

# ---------------- Navigation Logic ---------------- #
frame_history = []
forward_stack = []

def show_frame(name):
    frames[name].lift()

def navigate_to(name):
    if frame_history and frame_history[-1] == name:
        return
    frame_history.append(name)
    forward_stack.clear()
    show_frame(name)

def go_back():
    if len(frame_history) > 1:
        current = frame_history.pop()
        forward_stack.append(current)
        show_frame(frame_history[-1])

def go_forward():
    if forward_stack:
        next_frame = forward_stack.pop()
        frame_history.append(next_frame)
        show_frame(next_frame)

# ---------------- Create Pages ---------------- #
sidebar = create_sidebar(root, content_frame, frames, navigate_to, go_back, go_forward)

frames["Dashboard"] = create_dashboard(content_frame, navigate_to)
frames["Monitor"] = create_monitor_dashboard(content_frame)
frames["History"] = create_history(content_frame)
frames["Settings"] = create_settings(content_frame)
frames["ConfigureScan"] = create_scan(content_frame)
frames["Search"] = create_search(content_frame)
frames["CodeAnalysis"] = create_code_analysis(content_frame)
frames["Quarantine"] = create_quarantine(content_frame)
frames["Notifications"] = create_notification(content_frame)
frames["ML"] = create_ml_page(content_frame)
frames["User"] = create_user_profile(content_frame, user)

for frame in frames.values():
    frame.place(relwidth=1, relheight=1)
    frame.lower()

# ---------------- Default View ---------------- #
navigate_to("Monitor")

# ---------------- Start Application ---------------- #
root.mainloop()
