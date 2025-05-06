import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from svc.hybrid_analysis_api import analyze_with_hybrid_analysis
from svc.virustotal_api import analyze_with_virustotal

# Load .env
load_dotenv()
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
HA_API_KEY = os.getenv("HYBRID_ANALYSIS_API_KEY")

def create_code_analysis(parent):
    frame = tk.Frame(parent, bg="#0d0d0d")

    # --- Sidebar --- #
    sidebar = tk.Frame(frame, bg="#dbe7d2", width=300, height=700)
    sidebar.pack(side="left", fill="y", padx=20, pady=20)
    sidebar.pack_propagate(False)

    # --- Right Content Panel --- #
    content = tk.Frame(frame, bg="#000000", width=800, height=700)
    content.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)
    content.pack_propagate(False)

    # --- Variables --- #
    vt_var = tk.BooleanVar(value=True)
    ha_var = tk.BooleanVar(value=True)
    input_mode = tk.StringVar(value="code")
    filepath = tk.StringVar()

    # --- Terminal Output Area --- #
    terminal_output = tk.Text(content, height=10, bg="#000000", fg="#76ff03", font=("Consolas", 10), insertbackground="white")
    terminal_output.pack(padx=20, pady=(10, 0), fill="both", expand=True)
    terminal_output.insert(tk.END, "🔍 Output will appear here...\n")
    terminal_output.config(state="disabled")

    # --- File name label --- #
    filename_label = tk.Label(content, text="", font=("Segoe UI", 10), bg="#000000", fg="#76ff03")
    filename_label.pack(pady=(5, 0))

    # --- Code Text Area --- #
    code_text = tk.Text(content, height=10, width=80, bg="#1a1a1a", fg="white", insertbackground="white", font=("Consolas", 10))
    code_text.pack(pady=10)

    upload_btn = ttk.Button(content, text="Upload File", command=lambda: on_upload())

    def toggle_input_mode():
        if input_mode.get() == "code":
            code_text.pack(pady=10)
            upload_btn.pack_forget()
            filename_label.config(text="")
        else:
            code_text.pack_forget()
            upload_btn.pack(pady=10)

    def on_upload():
        selected_file = filedialog.askopenfilename()
        if selected_file:
            filepath.set(selected_file)
            filename_label.config(text=f"📄 Selected File: {os.path.basename(selected_file)}")
            log(f"File uploaded: {selected_file}")

    def log(message):
        terminal_output.config(state="normal")
        terminal_output.insert(tk.END, f"{message}\n")
        terminal_output.see(tk.END)
        terminal_output.config(state="disabled")

    def start_analysis():
        terminal_output.config(state="normal")
        terminal_output.delete("1.0", tk.END)
        terminal_output.config(state="disabled")

        file_path = ""
        selected_engines = []

        if vt_var.get():
            selected_engines.append("VirusTotal")
        if ha_var.get():
            selected_engines.append("HybridAnalysis")

        if input_mode.get() == "code":
            code = code_text.get("1.0", tk.END).strip()
            if not code:
                messagebox.showwarning("Empty Input", "Please enter some code.")
                return
            with open("temp_code.py", "w") as f:
                f.write(code)
            file_path = "temp_code.py"
            log("Code written to temp_code.py")
        else:
            if not filepath.get():
                messagebox.showwarning("No File", "Please select a file.")
                return
            file_path = filepath.get()
            log(f"Analyzing file: {file_path}")

        for engine in selected_engines:
            if engine == "VirusTotal":
                try:
                    vt_result = analyze_with_virustotal(file_path, VT_API_KEY)
                    log("✅ VirusTotal Result:")
                    log(vt_result)
                except Exception as e:
                    log(f"❌ VirusTotal Error: {e}")
            elif engine == "HybridAnalysis":
                try:
                    ha_result = analyze_with_hybrid_analysis(file_path, HA_API_KEY)
                    log("✅ Hybrid Analysis Result:")
                    for k, v in ha_result.items():
                        log(f"{k}: {v}")
                except Exception as e:
                    log(f"❌ Hybrid Analysis Error: {e}")

    # --- Sidebar Controls --- #
    tk.Label(sidebar, text="Code Analysis", font=("Segoe UI", 18, "bold"), bg="#dbe7d2", fg="#0d0d0d").pack(pady=(20, 10))

    tk.Checkbutton(sidebar, text="VirusTotal", variable=vt_var, bg="#dbe7d2", font=("Segoe UI", 11)).pack(pady=5, anchor="w", padx=20)
    tk.Checkbutton(sidebar, text="Hybrid Analysis", variable=ha_var, bg="#dbe7d2", font=("Segoe UI", 11)).pack(pady=5, anchor="w", padx=20)

    tk.Label(sidebar, text="Input Mode", font=("Segoe UI", 12, "bold"), bg="#dbe7d2").pack(pady=(20, 5), anchor="w", padx=20)
    tk.Radiobutton(sidebar, text="Code", variable=input_mode, value="code", command=toggle_input_mode, bg="#dbe7d2", font=("Segoe UI", 11)).pack(pady=2, anchor="w", padx=20)
    tk.Radiobutton(sidebar, text="File Upload", variable=input_mode, value="file", command=toggle_input_mode, bg="#dbe7d2", font=("Segoe UI", 11)).pack(pady=2, anchor="w", padx=20)

    tk.Button(sidebar, text="Start Analysis", command=start_analysis, bg="#1f1f1f", fg="white", font=("Segoe UI", 11), activebackground="#333333", activeforeground="white").pack(pady=30, padx=20, fill="x")

    toggle_input_mode()  # Set initial view

    return frame
