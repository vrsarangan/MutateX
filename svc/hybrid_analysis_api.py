import requests
import time

def analyze_with_hybrid_analysis(file_path, api_key):
    submit_url = "https://www.hybrid-analysis.com/api/v2/submit/file"
    headers = {
        "User-Agent": "Falcon Sandbox",
        "api-key": api_key
    }

    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "environment_id": "120"  # Windows 10 64-bit
        }

        # Submit the file
        response = requests.post(submit_url, headers=headers, files=files, data=data)
        if response.status_code != 200:
            raise Exception(f"Hybrid Analysis upload failed: {response.text}")

        result = response.json()
        sha256 = result.get("sha256")
        if not sha256:
            raise Exception("SHA256 not found in submission response.")

    # Poll the report using sha256
    report_url = f"https://www.hybrid-analysis.com/api/v2/overview/{sha256}"
    for _ in range(15):  # Try for ~75 seconds
        report_response = requests.get(report_url, headers=headers)
        if report_response.status_code == 200:
            report = report_response.json()
            return {
                "Submit Name": report.get("submit_name"),
                "SHA256": report.get("sha256"),
                "Threat Score": report.get("threat_score"),
                "Verdict": report.get("verdict"),
                "Tags": ", ".join(report.get("classification_tags", [])),
                "Analysis Link": f"https://www.hybrid-analysis.com/sample/{sha256}"
            }
        time.sleep(5)

    raise Exception("Timed out waiting for Hybrid Analysis report.")
