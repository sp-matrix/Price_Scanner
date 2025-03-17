#!/bin/bash

# Databricks configuration (these will be passed as parameters)
DATABRICKS_HOST=$1
DATABRICKS_TOKEN=$2
JOB_ID=$3
VALUES=($4)  # Expecting space-separated values as a single string

# Function to trigger a job
trigger_job() {
    local value=$1
    payload=$(cat <<EOF
{
    "job_id": "$JOB_ID",
    "notebook_params": {
        "input_value": "$value"
    }
}
EOF
)

    response=$(curl -s -X POST \
        -H "Authorization: Bearer $DATABRICKS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$DATABRICKS_HOST/api/2.1/jobs/run-now")

    run_id=$(echo "$response" | grep -o '"run_id":[0-9]*' | cut -d: -f2)
    if [ -n "$run_id" ]; then
        echo "Triggered job for value $value with run_id: $run_id"
    else
        echo "Error triggering job for value $value: $response"
    fi
}

# Export function for subshells
export -f trigger_job

# Trigger jobs in parallel
for value in "${VALUES[@]}"; do
    trigger_job "$value" &
    pids[${#pids[@]}]=$!
done

# Wait for all jobs to complete
for pid in ${pids[*]}; do
    wait $pid
done

echo "All jobs triggered"