import tkinter as tk
from ui.scan import create_scan  # Corrected import

def create_dashboard(parent, show_frame):
    frame = tk.Frame(parent, bg="#0d0d0d")  # Match main app background

    # Title
    tk.Label(frame, text="Predate", font=("Courier", 48, "bold"),
             fg="#4caf50", bg="#0d0d0d").place(x=150, y=50)

    # Tooltip label
    tooltip = tk.Label(frame, text="", bg="#333333", fg="white",
                       bd=1, relief="solid", font=("Arial", 10))
    tooltip.place_forget()

    # Tooltip logic
    def show_tooltip(event, text):
        tooltip.config(text=text)
        tooltip.place(x=event.x_root - frame.winfo_rootx() + 10,
                      y=event.y_root - frame.winfo_rooty() + 10)

    def hide_tooltip(event):
        tooltip.place_forget()

    # Scan animation label (initially hidden)
    scan_status = tk.Label(frame, text="", font=("Courier", 18),
                           bg="#0d0d0d", fg="#4caf50")
    scan_status.place(x=150, y=450)

    # Animate scan status
    def animate_scan(text, callback):
        dots = ["", ".", "..", "..."]
        i = 0

        def loop():
            nonlocal i
            scan_status.config(text=text + dots[i % 4])
            i += 1
            if i < 10:
                frame.after(300, loop)
            else:
                scan_status.config(text="")
                callback()

        loop()

    # Scan icon buttons with color inversion on hover
    icons_info = [
        ("⚡", "Quick Scan", lambda: animate_scan("Running Quick Scan", lambda: show_frame("QuickScan"))),
        ("🌍", "Full Scan", lambda: animate_scan("Performing Full System Scan", lambda: show_frame("FullScan"))),
        ("📄", "Configure Scan", lambda: animate_scan("Loading Scan Configuration", lambda: show_frame("ConfigureScan"))),
    ]

    for i, (icon, hint, command) in enumerate(icons_info):
        box = tk.Frame(frame, bg="#1e1e1e", width=120, height=120, cursor="hand2",
                       highlightthickness=2, highlightbackground="#4caf50")
        box.place(x=150 + i * 160, y=150)

        label = tk.Label(box, text=icon, bg="#1e1e1e", fg="#4caf50", font=("Arial", 48))
        label.place(relx=0.5, rely=0.5, anchor="center")

        def make_hover_funcs(b=box, l=label, t=hint, cmd=command):
            def on_enter(event):
                show_tooltip(event, t)
                b.config(bg="#4caf50")
                l.config(bg="#4caf50", fg="#0d0d0d")

            def on_leave(event):
                hide_tooltip(event)
                b.config(bg="#1e1e1e")
                l.config(bg="#1e1e1e", fg="#4caf50")

            def on_click(event):
                cmd()

            return on_enter, on_leave, on_click

        enter, leave, click = make_hover_funcs()

        for widget in [box, label]:
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
            widget.bind("<Button-1>", click)

    # Launch Sandbox Button
    tk.Button(frame, text="Launch Sandbox", bg="#4caf50", fg="#0d0d0d",
              font=("Arial", 24, "bold"), cursor="hand2", activebackground="#66bb6a",
              activeforeground="black", relief="flat").place(x=150, y=330, width=480, height=80)

    # Side feature buttons
    features = [
        ("🕒", "Scan History", lambda: show_frame("History")),
        ("⚠️", "Quarantine", lambda: show_frame("Quarantine")),
        ("</>", "Code Analysis", lambda: show_frame("CodeAnalysis"))
    ]
    for i, (icon, text, command) in enumerate(features):
        tk.Button(frame, text=f"{icon}\n{text}", bg="#1a1a1a", fg="#4caf50",
                  font=("Arial", 16, "bold"), relief="flat", justify="center",
                  command=command, cursor="hand2", activebackground="#2e2e2e",
                  activeforeground="#81c784").place(
            x=700, y=100 + i * 120, width=200, height=100)

    return frame
