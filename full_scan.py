import time
import random

def run_full_scan(progress_callback=None, done_callback=None):
    total_steps = 50
    for step in range(total_steps):
        time.sleep(0.3)
        if progress_callback:
            percent = int((step + 1) / total_steps * 100)
            time_left = round((total_steps - step - 1) * 0.3, 1)
            progress_callback(percent, f"{time_left}s")
    if done_callback:
        done_callback()
