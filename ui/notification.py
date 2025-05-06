import tkinter as tk

def create_notification(parent):
    # --- Main Notification Frame --- #
    notification_frame = tk.Frame(parent, bg="#0d0d0d")

    # Left Panel: Notification List
    list_panel = tk.Frame(notification_frame, bg="#dbe7d2", width=300, height=700)
    list_panel.pack(side="left", fill="y", padx=20, pady=20)
    list_panel.pack_propagate(False)

    # Right Panel: Notification Detail
    detail_panel = tk.Frame(notification_frame, bg="#000000", width=800, height=700)
    detail_panel.pack(side="left", expand=True, fill="both", padx=(0, 20), pady=20)
    detail_panel.pack_propagate(False)

    # Header on right panel
    header = tk.Label(detail_panel, text="🔔 Notifications", font=("Segoe UI", 28, "bold"),
                      fg="#76ff03", bg="#000000")
    header.pack(pady=(30, 10))

    # Detail content label (dynamic)
    detail_title = tk.Label(detail_panel, text="", font=("Segoe UI", 18, "bold"),
                            fg="#4caf50", bg="#000000", anchor="w", wraplength=700)
    detail_title.pack(fill="x", padx=30, pady=(10, 0))

    detail_message = tk.Label(detail_panel, text="", font=("Segoe UI", 13),
                              fg="white", bg="#000000", anchor="nw", justify="left", wraplength=700)
    detail_message.pack(fill="both", expand=True, padx=30, pady=(5, 20))

    # Sample Notifications
    notifications = [
        ("System Scan Complete", "Your scheduled system scan completed with no threats found.", "🛡️"),
        ("New Device Login", "A new device logged into your account from Colombo, SL.", "📍"),
        ("Update Available", "A new version of the antivirus engine is available. Please update.", "⬇️"),
        ("Firewall Alert", "Suspicious inbound connection attempt blocked by the firewall.", "🚫"),
        ("Backup Reminder", "Your last backup was 7 days ago. Consider backing up your data.", "💾"),
        ("Subscription Notice", "Your subscription will expire in 5 days. Renew to stay protected.", "⏳"),
    ]

    def show_detail(title, message, icon):
        detail_title.config(text=f"{icon} {title}")
        detail_message.config(text=message)

    # Add buttons to left list panel
    for title, message, icon in notifications:
        btn = tk.Button(
            list_panel,
            text=f"{icon} {title}",
            font=("Segoe UI", 11, "bold"),
            bg="#1f1f1f",
            fg="#76ff03",
            relief="flat",
            activebackground="#333333",
            activeforeground="white",
            anchor="w",
            justify="left",
            wraplength=280,
            padx=10,
            pady=10,
            command=lambda t=title, m=message, i=icon: show_detail(t, m, i)
        )
        btn.pack(fill="x", pady=5, padx=10)

    # Show first notification by default
    if notifications:
        first = notifications[0]
        show_detail(*first)

    return notification_frame
