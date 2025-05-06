import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import stat
import platform
import subprocess

SECURE_DIR = os.path.expanduser("~/secure_quarantine")

def create_quarantine(parent):
    # Create secure quarantine folder
    os.makedirs(SECURE_DIR, exist_ok=True)
    if platform.system() == "Windows":
        subprocess.run(['attrib', '+H', '+R', SECURE_DIR])
    else:
        os.chmod(SECURE_DIR, 0o700)

    # Main Quarantine Frame
    quarantine_frame = tk.Frame(parent, bg="#0d0d0d")

    # Left Sidebar
    sidebar = tk.Frame(quarantine_frame, bg="#dbe7d2", width=300, height=700)
    sidebar.pack(side="left", fill="y", padx=20, pady=20)
    sidebar.pack_propagate(False)

    # Right Content Panel
    content_panel = tk.Frame(quarantine_frame, bg="#000000", width=800, height=700)
    content_panel.pack(side="left", expand=True, fill="both", padx=(0, 20), pady=20)
    content_panel.pack_propagate(False)

    # Quarantine Title
    title_label = tk.Label(content_panel, text="🛡️ Quarantine Center", font=("Segoe UI", 24, "bold"), fg="#76ff03", bg="#000000")
    title_label.pack(pady=(20, 10))

    # File List Display
    listbox = tk.Listbox(content_panel, font=("Courier", 12), width=70, bg="#1a1a1a", fg="#76ff03", selectbackground="#333333", borderwidth=0, highlightthickness=0)
    listbox.pack(pady=10, padx=20)

    def refresh_list():
        listbox.delete(0, tk.END)
        for file in os.listdir(SECURE_DIR):
            listbox.insert(tk.END, file)

    def quarantine_file():
        filepath = filedialog.askopenfilename(title="Select File to Quarantine")
        if filepath:
            try:
                filename = os.path.basename(filepath)
                quarantine_path = os.path.join(SECURE_DIR, filename)

                if os.path.exists(quarantine_path):
                    messagebox.showwarning("Already Quarantined", f"{filename} is already quarantined.")
                    return

                shutil.move(filepath, quarantine_path)

                if platform.system() != "Windows":
                    os.chmod(quarantine_path, stat.S_IRUSR | stat.S_IWUSR)
                else:
                    base, ext = os.path.splitext(quarantine_path)
                    os.rename(quarantine_path, base + ".quarantine")

                messagebox.showinfo("Quarantined", f"{filename} quarantined securely.")
                refresh_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to quarantine: {e}")

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return
        filename = listbox.get(selection[0])
        full_path = os.path.join(SECURE_DIR, filename)
        try:
            os.remove(full_path)
            messagebox.showinfo("Deleted", f"{filename} permanently deleted.")
            refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}")

    def restore_selected():
        selection = listbox.curselection()
        if not selection:
            return
        filename = listbox.get(selection[0])
        full_path = os.path.join(SECURE_DIR, filename)
        new_path = filedialog.askdirectory(title="Restore to folder")
        if new_path:
            try:
                shutil.move(full_path, os.path.join(new_path, filename))
                messagebox.showinfo("Restored", f"{filename} restored to {new_path}")
                refresh_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore file: {e}")

    # Buttons
    button_style = {
        "font": ("Segoe UI", 12, "bold"),
        "width": 25,
        "padx": 10,
        "pady": 10,
        "bd": 0,
        "activebackground": "#333333",
        "activeforeground": "white",
    }

    tk.Button(content_panel, text="➕ Quarantine New File", command=quarantine_file,
              bg="#ff6666", fg="white", **button_style).pack(pady=5)

    tk.Button(content_panel, text="🗑️ Delete Selected File", command=delete_selected,
              bg="#cc0000", fg="white", **button_style).pack(pady=5)

    tk.Button(content_panel, text="♻️ Restore Selected File", command=restore_selected,
              bg="#009688", fg="white", **button_style).pack(pady=5)

    # Sidebar info or branding
    tk.Label(sidebar, text="Quarantine Info", font=("Segoe UI", 14, "bold"), bg="#dbe7d2", fg="#1a1a1a").pack(pady=20)
    tk.Label(sidebar, text="Files here are isolated\nand made harmless.", font=("Segoe UI", 11), bg="#dbe7d2", fg="#333333").pack()

    refresh_list()
    return quarantine_frame
