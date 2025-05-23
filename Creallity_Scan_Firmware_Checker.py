#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import hmac
import hashlib
import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Ensure script always runs relative to its own directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# === CONFIGURABLE VARIABLES ===
API_KEY = "5e77824b9a2e1e1650bcf3cef1f927a7"
API_SECRET = "a0e8eb55922e5d9d6831d8c63bc83f6f"
BASE_URL = "https://vcp.developer.orbbec.com.cn"
MANUFACTURER = "Creality"
MAX_WORKERS = 10
SINGLE_PID = 0
START_PID = 0
END_PID = 9999
API_TIMEOUT = 4
RESULTS_FILE = "firmware_results.txt"

# Shared results list and lock for thread-safe updates
results = []
results_lock = Lock()


# === UTILITY FUNCTIONS ===
def generate_signature(timestamp: str, key: str, secret: str) -> str:
    message = f"{key}\n{timestamp}\n"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def write_results_to_file():
    """Writes all results to the results file, sorted by PID."""
    sorted_results = sorted(results, key=lambda x: x[0])
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        for pid, data in sorted_results:
            version = data.get("version", "N/A")
            f.write(f"PID: {pid}\n")
            f.write(f"Latest Firmware Version: {version}\n")
            f.write(f"Full Info: {data}\n")
            f.write("-" * 55 + "\n")


def get_fire_version(session: requests.Session, pid: int, manufacturer: str):
    endpoint = "/ota_api/v1/fire_version"
    url = f"{BASE_URL}{endpoint}"

    timestamp = str(int(time.time()))
    signature = generate_signature(timestamp, API_KEY, API_SECRET)

    headers = {
        "Content-Type": "application/json",
        "X-Ca-Key": API_KEY,
        "System-time": timestamp,
        "X-Ca-Signature": signature,
    }

    params = {
        "pid": pid,
        "new_version_flag": True,
        "customer": manufacturer,
    }

    try:
        response = session.get(url, headers=headers, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 0:
            with results_lock:
                results.append((pid, data["data"]))
                write_results_to_file()

            return pid, data["data"]

    except Exception as e:
        print(f"[ERROR] PID={pid} - {e}")
    
    return pid, None


# === MAIN FUNCTION ===
def main():
    use_range = SINGLE_PID in (None, 0)
    pids_to_check = range(START_PID, END_PID + 1) if use_range else [SINGLE_PID]

    # Clear file at start
    with open(RESULTS_FILE, "w", encoding="utf-8"):
        pass

    with requests.Session() as session:
        if not use_range:
            pid, result = get_fire_version(session, SINGLE_PID, MANUFACTURER)
            print(f"PID: {pid} => Waiting for response...")
            if result:
                print(f"PID: {pid} => Firmware info: {result}")
                version = result.get("version")
                if version:
                    print(f"PID: {pid} => Latest firmware version: {version}")
        else:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {
                    executor.submit(get_fire_version, session, pid, MANUFACTURER): pid
                    for pid in pids_to_check
                }

                for future in as_completed(futures):
                    pid, result = future.result()
                    print(f"PID: {pid} => Waiting for response...")
                    if result:
                        print(f"PID: {pid} => Firmware info: {result}")
                        version = result.get("version")
                        if version:
                            print(f"PID: {pid} => Latest firmware version: {version}")
                        print("-" * 55)


# === SCRIPT ENTRY POINT ===
if __name__ == "__main__":
    main()
