import os
import time
import psutil
import csv
import hashlib
from scapy.all import sniff
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread

# ========== CONFIG ==========
MONITOR_FOLDER = "C:\\Users\\User\\Documents\\MutateX\\ML\\monitor_folder"
LABEL = "NORMAL"  # <-- CHANGE this before running!
csv_path = r"C:\Users\User\Documents\MutateX\ML\behavior_logs.csv"

# Ensure directory for CSV exists
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# ========== Global counters ==========
file_created_count = 0
file_deleted_count = 0
file_modified_count = 0
packet_count = 0
previous_hashes = {}

# ========== File system event handler ==========
class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        global file_created_count
        if not event.is_directory:
            file_created_count += 1
            previous_hashes[event.src_path] = file_hash(event.src_path)

    def on_deleted(self, event):
        global file_deleted_count
        if not event.is_directory:
            file_deleted_count += 1
            if event.src_path in previous_hashes:
                del previous_hashes[event.src_path]

    def on_modified(self, event):
        global file_modified_count
        if not event.is_directory:
            new_hash = file_hash(event.src_path)
            if previous_hashes.get(event.src_path) != new_hash:
                file_modified_count += 1
                previous_hashes[event.src_path] = new_hash

# ========== Helper to hash files ==========
def file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None  # file might be temporarily locked

# ========== Network packet sniffer ==========
def packet_callback(packet):
    global packet_count
    packet_count += 1

def start_sniffing():
    sniff(prn=packet_callback, store=0)

# ========== Initialize folder monitoring ==========
def start_monitoring_folder():
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_FOLDER, recursive=True)
    observer.start()
    return observer

# ========== Behavior logger ==========
def start_logging():
    global file_created_count, file_deleted_count, file_modified_count, packet_count

    # Create CSV file with headers if it doesn't exist
    if not os.path.exists(csv_path):
        with open(csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp", "CPU_Usage", "Memory_Usage", "Processes_Spawned",
                "Files_Created", "Files_Deleted", "Files_Modified", 
                "Packets_Captured", "Active_Connections", "New_Processes_Spawned", "label"
            ])

    previous_processes = set(psutil.pids())

    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        current_processes = set(psutil.pids())
        new_processes = len(current_processes - previous_processes)
        previous_processes = current_processes

        try:
            connections = psutil.net_connections()
            active_connections = sum(1 for conn in connections if conn.status == "ESTABLISHED")
        except Exception:
            active_connections = 0

        with open(csv_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, cpu_usage, memory_usage, len(current_processes),
                file_created_count, file_deleted_count, file_modified_count, 
                packet_count, active_connections, new_processes, LABEL
            ])

        print(f"[{timestamp}] CPU: {cpu_usage}% | Mem: {memory_usage}% | "
              f"Proc: {len(current_processes)} | New Proc: {new_processes} | "
              f"Files C:{file_created_count} D:{file_deleted_count} M:{file_modified_count} | "
              f"Packets: {packet_count} | Conn: {active_connections}")

        file_created_count = 0
        file_deleted_count = 0
        file_modified_count = 0
        packet_count = 0

        time.sleep(4)

# ========== Main ==========
if __name__ == "__main__":
    print("🔵 Starting file system monitoring...")
    observer = start_monitoring_folder()

    print("🔵 Starting network packet sniffing...")
    sniff_thread = Thread(target=start_sniffing)
    sniff_thread.daemon = True
    sniff_thread.start()

    print(f"🔵 Behavior logging started with label: {LABEL}")
    try:
        start_logging()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("🛑 Stopped.")
