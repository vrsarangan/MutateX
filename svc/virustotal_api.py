import requests
import hashlib
import time
import os

def analyze_with_virustotal(file_path, api_key):
    headers = {
        "x-apikey": api_key
    }

    # Upload the file
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post("https://www.virustotal.com/api/v3/files", files=files, headers=headers)

    if response.status_code != 200:
        raise Exception(f"VirusTotal upload failed: {response.text}")

    analysis_id = response.json()["data"]["id"]

    # Wait for analysis completion
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    for _ in range(10):
        result = requests.get(analysis_url, headers=headers).json()
        status = result["data"]["attributes"]["status"]
        if status == "completed":
            break
        time.sleep(2)
    else:
        raise Exception("VirusTotal analysis timed out")

    # Calculate SHA256 to get full report
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()

    # Fetch full file report
    report_url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"
    report_response = requests.get(report_url, headers=headers)
    if report_response.status_code != 200:
        raise Exception(f"Failed to fetch detailed report: {report_response.text}")

    data = report_response.json()["data"]["attributes"]

    # Extract detailed results
    result = {
        "File Name": os.path.basename(file_path),
        "MD5": data.get("md5"),
        "SHA1": data.get("sha1"),
        "SHA256": data.get("sha256"),
        "File Type": data.get("type_description"),
        "Size (bytes)": data.get("size"),
        "First Submitted": data.get("first_submission_date"),
        "Last Analysis Date": data.get("last_analysis_date"),
        "Meaningful Name": data.get("meaningful_name"),
        "Malicious": data.get("last_analysis_stats", {}).get("malicious"),
        "Suspicious": data.get("last_analysis_stats", {}).get("suspicious"),
        "Harmless": data.get("last_analysis_stats", {}).get("harmless"),
        "Undetected": data.get("last_analysis_stats", {}).get("undetected")
    }

    return "\n".join([f"{k}: {v}" for k, v in result.items()])
