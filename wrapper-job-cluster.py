import json
from concurrent.futures import ThreadPoolExecutor
import dbutils

# Function to run a notebook
def run_notebook(notebook_path, params):
    try:
        result = dbutils.notebook.run(notebook_path, timeout_seconds=3600, arguments=params)
        return f"Notebook {notebook_path} completed with result: {result}"
    except Exception as e:
        return f"Notebook {notebook_path} failed with error: {str(e)}"

# Get parameters passed via "Run Now" API
# Assuming parameters are passed as a JSON string
params = dbutils.widgets.get("parameters")
param_dict = json.loads(params)  # Parse the JSON string into a dictionary

# Example parameter structure: {"tasks": [{"notebook": "/path/to/notebook1", "params": {"key": "value"}}, ...]}
tasks = param_dict.get("tasks", [])

# List to store notebook execution tasks
notebook_tasks = []

# Prepare notebook runs based on parameters
for task in tasks:
    notebook_path = task.get("notebook")
    notebook_params = task.get("params", {})
    if notebook_path:
        notebook_tasks.append((notebook_path, notebook_params))

# Execute notebooks in parallel using ThreadPoolExecutor
results = []
with ThreadPoolExecutor(max_workers=len(notebook_tasks)) as executor:
    # Submit all notebook runs
    future_to_notebook = {executor.submit(run_notebook, path, params): path for path, params in notebook_tasks}
    # Collect results as they complete
    for future in future_to_notebook:
        notebook_path = future_to_notebook[future]
        try:
            result = future.result()
            results.append(result)
        except Exception as e:
            results.append(f"Error executing {notebook_path}: {str(e)}")

# Output results
for result in results:
    print(result)

# Exit the wrapper job
dbutils.notebook.exit("Wrapper job completed")