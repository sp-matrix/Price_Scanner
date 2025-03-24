import json
import threading
from databricks.sdk import WorkspaceClient
from datetime import datetime

class NotebookRunner:
    def __init__(self):
        # Initialize Databricks workspace client
        self.workspace = WorkspaceClient()

    def run_notebook(self, notebook_path, email, threshold_time):
        """Run a single notebook with built-in Databricks notifications"""
        try:
            # Submit notebook as a job with notification settings
            run = self.workspace.jobs.submit(
                run_name=f"Notebook_{notebook_path}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                tasks=[{
                    "task_key": f"run_{notebook_path}",
                    "notebook_task": {
                        "notebook_path": notebook_path
                    },
                    # Built-in notification settings for this task
                    "email_notifications": {
                        "on_start": [],  # No emails on start
                        "on_success": [email],
                        "on_failure": [email],
                        "on_duration_warning_threshold_exceeded": [email]
                    },
                    # Set the threshold for duration warning
                    "max_duration_seconds": threshold_time
                }]
            )

            # Optionally monitor the run (if you still want custom logic)
            run_id = run.run_id
            status = self.workspace.jobs.get_run(run_id=run_id)
            print(f"Started notebook {notebook_path} with run_id {run_id}")

        except Exception as e:
            print(f"Failed to start notebook {notebook_path}: {str(e)}")

    def process_notebooks(self, notebook_list):
        """Process multiple notebooks concurrently"""
        threads = []
        
        for notebook in notebook_list:
            notebook_path = notebook['notebook_name']
            email = notebook['email']
            threshold_time = notebook['threshold_time']
            
            # Create and start a thread for each notebook
            thread = threading.Thread(
                target=self.run_notebook,
                args=(notebook_path, email, threshold_time)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete (optional)
        for thread in threads:
            thread.join()

def main():
    # Example API endpoint handler
    def api_handler(event):
        # Parse API input
        notebook_list = json.loads(event['body'])
        
        # Create runner instance
        runner = NotebookRunner()
        
        # Process all notebooks
        runner.process_notebooks(notebook_list)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Notebooks triggered successfully'})
        }

    # Example invocation (for testing)
    sample_event = {
        'body': json.dumps([
            {
                'notebook_name': '/Users/user/notebook1',
                'email': 'user1@example.com',
                'threshold_time': 300  # 5 minutes
            },
            {
                'notebook_name': '/Users/user/notebook2',
                'email': 'user2@example.com',
                'threshold_time': 600  # 10 minutes
            }
        ])
    }
    
    # Test the handler
    result = api_handler(sample_event)
    print(result)

if __name__ == "__main__":
    main()