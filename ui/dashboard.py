import tkinter as tk

def create_dashboard(parent):
    frame = tk.Frame(parent, bg="#a4d4ae")

    # Title
    tk.Label(frame, text="Predate", font=("Courier", 48, "bold"), fg="#1a1a1a", bg="#a4d4ae").place(x=150, y=50)

    # Big icon boxes
    icons = ["⚡", "🌍", "📄"]
    for i, icon in enumerate(icons):
        box = tk.Frame(frame, bg="#e0e0e0", width=120, height=120)
        box.place(x=150 + i * 160, y=150)
        tk.Label(box, text=icon, bg="#e0e0e0", font=("Arial", 48)).place(relx=0.5, rely=0.5, anchor="center")

    # Big Launch Sandbox button
    tk.Button(frame, text="Launch Sandbox", bg="#4caf50", fg="black", font=("Arial", 24, "bold")).place(x=150, y=330, width=480, height=80)

    # Big feature buttons
    features = [("🕒", "Scan History"), ("⚠️", "Quarantine"), ("</>", "Code Analysis")]
    for i, (icon, text) in enumerate(features):
        tk.Button(frame, text=f"{icon}\n{text}", bg="#1a1a1a", fg="#4caf50",
                  font=("Arial", 16, "bold"), relief="flat", justify="center").place(x=700, y=100 + i * 120, width=200, height=100)

    # Bigger top right icons
    for i, icon in enumerate(["🔍", "🔔", "⚙️"]):
        tk.Label(frame, text=icon, bg="#a4d4ae", font=("Arial", 20)).place(x=950 + i * 40, y=20)

    return frame
