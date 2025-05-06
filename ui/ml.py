import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os

# Adjust these paths as needed
BEHAVIOR_LOGGER_SCRIPT = os.path.join("ml", "behavior_logger.py")
TRAIN_MODEL_SCRIPT = os.path.join("ml", "train_model.py")

logger_process = None

def create_ml_page(parent):
    frame = tk.Frame(parent, bg="#1e1e1e")

    title = tk.Label(frame, text="🧠 ML Behavior Trainer", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="#ffffff")
    title.pack(pady=20)

    status_label = tk.Label(frame, text="Status: Idle", fg="cyan", bg="#1e1e1e", font=("Arial", 12))
    status_label.pack(pady=10)

    def run_logger():
        global logger_process
        if logger_process is None:
            def start_logger():
                global logger_process
                os.environ["LABEL"] = "benign"
                logger_process = subprocess.Popen(["python", BEHAVIOR_LOGGER_SCRIPT])
                status_label.config(text="Recording behavior...")
            threading.Thread(target=start_logger, daemon=True).start()
        else:
            messagebox.showinfo("Info", "Logger is already running.")

    def stop_logger():
        global logger_process
        if logger_process:
            logger_process.terminate()
            logger_process = None
            status_label.config(text="Logger stopped.")
        else:
            messagebox.showinfo("Info", "Logger is not running.")

    def train_model():
        def run_training():
            status_label.config(text="Training model...")
            try:
                subprocess.run(["python", TRAIN_MODEL_SCRIPT], check=True)
                messagebox.showinfo("Success", "Model trained and saved successfully.")
                status_label.config(text="Model training completed.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Model training failed.")
                status_label.config(text="Training failed.")
        threading.Thread(target=run_training, daemon=True).start()

    # Buttons
    tk.Button(frame, text="▶ Start Recording Behavior", command=run_logger, width=30, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
    tk.Button(frame, text="⏹ Stop Recording", command=stop_logger, width=30, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=5)
    tk.Button(frame, text="🔁 Train Model", command=train_model, width=30, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=5)

    return frame
