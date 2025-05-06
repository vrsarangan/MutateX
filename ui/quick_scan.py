import time
import random

def run_quick_scan(progress_callback=None, done_callback=None):
    total_steps = 20
    for step in range(total_steps):
        time.sleep(0.2)  # simulate scanning delay
        if progress_callback:
            percent = int((step + 1) / total_steps * 100)
            time_left = round((total_steps - step - 1) * 0.2, 1)
            progress_callback(percent, f"{time_left}s")
    if done_callback:
        done_callback()
