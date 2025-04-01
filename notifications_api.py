import requests
from concurrent.futures import ThreadPoolExecutor
import json

# Configuration: Map report names to notebook paths and emails
report_config = {
    "Report1": {
        "path": "/Users/yourname/Report1",
        "emails": ["team1@example.com"]
    },
    "Report2": {
        "path": "/Users/yourname/Report2",
        "emails": ["team2@example.com"]
    },
    "Report3": {
        "path": "/Users/yourname/Report3",
        "emails": ["team3@example.com"]
    }
    # Add more as needed
}

# Databricks API token and instance (for notifications)
token = dbutils.secrets.get(scope="your-scope", key="your-token")
databricks_instance = "https://<your-databricks-instance>"
headers = {"Authorization": f"Bearer {token}"}

# Function to send notification via Databricks REST API (optional, requires webhook setup)
def send_notification(message, recipients):
    # If your admin has set up a notification destination, use this
    # Otherwise, skip this and rely on sub-notebook logic
    try:
        response = requests.post(
            f"{databricks_instance}/api/2.0/notification/messages",
            headers=headers,
            json={
                "recipients": recipients,
                "message": message
            }
        )
        if response.status_code != 200:
            print(f"Failed to send notification: {response.text}")
    except Exception as e:
        print(f"Notification error: {str(e)}")

# Function to run a notebook and handle notifications
def run_notebook(report_name):
    if report_name not in report_config:
        error_msg = f"Error: No configuration for {report_name}"
        print(error_msg)
        return {"report": report_name, "status": "error", "message": error_msg}
    
    config = report_config[report_name]
    notebook_path = config["path"]
    recipients = config["emails"]

    # Send start notification
    start_msg = f"Notebook {report_name} started on cluster {dbutils.notebook.entry_point.getDbutils().notebook().getContext().clusterId().get()}"
    send_notification(start_msg, recipients)
    print(start_msg)

    try:
        # Run the notebook on the same cluster
        result = dbutils.notebook.run(notebook_path, timeout_seconds=600)
        # Send success notification
        success_msg = f"Notebook {report_name} completed successfully"
        send_notification(success_msg, recipients)
        return {"report": report_name, "status": "success", "result": result}
    except Exception as e:
        # Send failure notification
        failure_msg = f"Notebook {report_name} failed: {str(e)}"
        send_notification(failure_msg, recipients)
        return {"report": report_name, "status": "failure", "error": str(e)}

# Get report names from API parameter
try:
    report_names = dbutils.widgets.get("report_names")  # e.g., "Report1,Report2"
    report_list = report_names.split(",")
except:
    # Fallback for testing
    report_list = ["Report1", "Report2"]  # Replace with your test list

# Run notebooks in parallel on the same cluster
with ThreadPoolExecutor() as executor:
    results = list(executor.map(run_notebook, report_list))

# Output results for debugging or API response
dbutils.notebook.exit(json.dumps({"triggered": report_list, "results": results}))