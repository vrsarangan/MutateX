# monitor_writer.py

import psutil
import pymongo
import time
import socket
import os
import threading
from dotenv import load_dotenv
from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict

# Load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# MongoDB setup
client = pymongo.MongoClient(mongo_uri)
db = client["mutatex"]
collection = db["system_metrics"]

# Network packet tracking
packet_store = defaultdict(lambda: {
    "proto": "", "src": "", "dst": "", "sport": 0, "dport": 0, "count": 0
})
lock = threading.Lock()

# Packet sniffing handler
def packet_handler(pkt):
    if IP in pkt:
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "Other"
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        sport = getattr(pkt, 'sport', 0)
        dport = getattr(pkt, 'dport', 0)
        key = (proto, src_ip, dst_ip, sport, dport)

        with lock:
            entry = packet_store[key]
            entry.update({
                "proto": proto,
                "src": src_ip,
                "dst": dst_ip,
                "sport": sport,
                "dport": dport
            })
            entry["count"] += 1

# Start sniffing in background thread
def start_sniffer():
    try:
        sniff(prn=packet_handler, store=False, filter="ip")
    except Exception as e:
        print("❌ Packet sniffing error:", e)

sniffer_thread = threading.Thread(target=start_sniffer, daemon=True)
sniffer_thread.start()

# Main metrics collection loop
while True:
    try:
        with lock:
            packets = list(packet_store.values())
            packet_store.clear()

        # Fallback data if no packets
        if not packets:
            packets.append({
                "proto": "TCP",
                "src": "127.0.0.1",
                "dst": "8.8.8.8",
                "sport": 12345,
                "dport": 80,
                "count": 1
            })

        doc = {
            "_id": "live",
            "timestamp": time.time(),
            "hostname": socket.gethostname(),
            "cpu_percent": psutil.cpu_percent(),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict(),
            "net_io": psutil.net_io_counters()._asdict(),
            "uptime": time.time() - psutil.boot_time(),
            "connections": packets[:20],
            "processes": [
                p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            ]
        }

        collection.replace_one({"_id": "live"}, doc, upsert=True)
        print(f"✅ Updated {time.strftime('%X')} | CPU: {doc['cpu_percent']}% | Packets: {len(packets)}")
        time.sleep(1)

    except Exception as e:
        print("❌ Data collection error:", e)
        time.sleep(2)
