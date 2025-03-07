import requests
import json

# Replace with your Databricks workspace URL and token
DATABRICKS_INSTANCE = 'https://<databricks-instance>'
TOKEN = 'your-databricks-token'

# Define the headers for the API request
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# Function to trigger a job
def trigger_job(job_id):
    url = f'{DATABRICKS_INSTANCE}/api/2.1/jobs/run-now'
    payload = {
        'job_id': job_id
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f'Successfully triggered job {job_id}')
    else:
        print(f'Failed to trigger job {job_id}: {response.text}')

# List of job IDs to trigger
job_ids = [1234, 5678, 91011]  # Replace with your job IDs

# Trigger each job
for job_id in job_ids:
    trigger_job(job_id)