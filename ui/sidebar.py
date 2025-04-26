import tkinter as tk

def create_sidebar(root, content_frame, frames, show_frame_callback):
    sidebar_expanded = False
    sidebar_width_collapsed = 60
    sidebar_width_expanded = 200
    current_sidebar_width = sidebar_width_collapsed

    BUTTON_COLOR = "#1a1a1a"
    TEXT_GREEN = "#4caf50"

    sidebar_items = [
        ("☰", "Toggle"),
        ("🕒", "History"),
        ("🧪", "Scan"),
        ("🐛", "Dashboard"),
        ("📈", "Monitor"),
        ("⚙️", "Settings"),
        ("🔍", "Search")
    ]

    sidebar = tk.Frame(root, bg=BUTTON_COLOR, width=current_sidebar_width, height=800)
    sidebar.place(x=0, y=0)

    sidebar_buttons = []

    def toggle_sidebar():
        nonlocal sidebar_expanded, current_sidebar_width
        sidebar_expanded = not sidebar_expanded
        current_sidebar_width = sidebar_width_expanded if sidebar_expanded else sidebar_width_collapsed
        sidebar.config(width=current_sidebar_width)
        for btn, (icon, label) in zip(sidebar_buttons, sidebar_items):
            if sidebar_expanded:
                btn.config(text=f"{icon}  {label}", anchor="w", padx=10)
            else:
                btn.config(text=icon, anchor="center", padx=0)
            btn.place_configure(width=current_sidebar_width)

    def on_click(name, index):
        if name == "Toggle":
            toggle_sidebar()
            return
        actual_page = name  # No replacement needed now
        show_frame_callback(actual_page)
        for btn in sidebar_buttons:
            btn.config(bg=BUTTON_COLOR)
        sidebar_buttons[index].config(bg=TEXT_GREEN)

    for idx, (icon, label) in enumerate(sidebar_items):
        btn = tk.Button(
            sidebar,
            text=icon,
            fg="white",
            bg=BUTTON_COLOR,
            font=("Arial", 14),
            bd=0,
            command=lambda name=label, index=idx: on_click(name, index),
            activebackground="#333",
            anchor="center"
        )
        btn.place(x=0, y=50 + idx * 60, width=current_sidebar_width, height=40)
        sidebar_buttons.append(btn)

    tk.Label(sidebar, text="👤", bg=BUTTON_COLOR, fg="white", font=("Arial", 20)).place(x=15, y=680)

    return sidebar
