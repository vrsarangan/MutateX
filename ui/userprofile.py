import tkinter as tk

def create_user_profile(content_frame, user, show_frame=None, frames=None):
    # Main container
    user_profile_frame = tk.Frame(content_frame, bg="#0d0d0d")
    user_profile_frame.pack(fill=tk.BOTH, expand=True)


    # Content Panel
    content_panel = tk.Frame(user_profile_frame, bg="#121212")
    content_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    content_panel.pack_propagate(False)

    # Header
    header = tk.Label(content_panel, text="User Profile", bg="#121212", fg="#4caf50",
                      font=("Segoe UI", 20, "bold"))
    header.pack(pady=(10, 20))

    # Profile Card
    profile_card = tk.Frame(content_panel, bg="#1e1e1e", bd=0, relief="flat")
    profile_card.pack(pady=10, padx=20, fill="x", ipadx=10, ipady=10)

    # Profile picture placeholder
    avatar = tk.Label(profile_card, text="👤", font=("Arial", 48), bg="#1e1e1e", fg="white")
    avatar.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

    # User Details
    def add_label(row, text, value):
        label = tk.Label(profile_card, text=f"{text}: ", fg="#76ff03", bg="#1e1e1e",
                         font=("Segoe UI", 12, "bold"), anchor="w")
        label_val = tk.Label(profile_card, text=value, fg="white", bg="#1e1e1e",
                             font=("Segoe UI", 12), anchor="w")
        label.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        label_val.grid(row=row, column=2, sticky="w", padx=5, pady=5)

    add_label(0, "Name", user['name'])
    add_label(1, "Email", user['email'])
    add_label(2, "Role", user['role'])
    add_label(3, "Privilege", user['privilege'])
    add_label(4, "Phone", user['phone'])
    add_label(5, "Department", user['department'])
    add_label(6, "Last Login", user['last_login'])
    add_label(7, "Account Created", user['created_at'])

    # Buttons Frame
    btn_frame = tk.Frame(content_panel, bg="#121212")
    btn_frame.pack(pady=20)

    def reset_password():
        print("Resetting password...")

    def log_out():
        print("Logging out...")

    def create_button(text, command):
        return tk.Button(btn_frame, text=text, command=command,
                         font=("Segoe UI", 12), bg="#333", fg="#76ff03",
                         activebackground="#444", activeforeground="white",
                         relief="flat", padx=20, pady=10, bd=0, cursor="hand2")

    reset_button = create_button("Reset Password", reset_password)
    reset_button.grid(row=0, column=0, padx=10)

    logout_button = create_button("Log Out", log_out)
    logout_button.grid(row=0, column=1, padx=10)

    return user_profile_frame
