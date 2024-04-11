#!/bin/bash

# Define your conda environment name
CONDA_ENV_NAME="Hardin-Helper-AI"

# Define log file paths
FASTAPI_LOG="backend/fastapi.log"
NPM_LOG="npm-start.log"

# Ensure the log files exist and are empty
> "$FASTAPI_LOG"
> "$NPM_LOG"

# Activate your conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV_NAME"

# Check if Gunicorn is installed, install if not
if ! command -v gunicorn &> /dev/null
then
    echo "Gunicorn could not be found, installing..."
    conda install gunicorn -y || pip install gunicorn uvicorn[standard]
fi

# Change directory to the backend directory (still named flask-backend for your setup)
cd backend/

# Start Gunicorn with a single worker to allow it to claim the GPU
tmux new-session -d -s my_session "gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 --log-level info > ../$FASTAPI_LOG 2>&1"
echo "FastAPI application started with a single Gunicorn Uvicorn worker."

# Wait for a sufficient amount of time to ensure the first worker has fully initialized and potentially claimed GPU resources
sleep 2

# Number of additional workers to start
NUM_ADDITIONAL_WORKERS=0

# Start additional workers
for ((i = 1; i <= NUM_ADDITIONAL_WORKERS; i++))
do
    tmux send-keys -t my_session "kill -TTIN \$(pgrep -f gunicorn)" C-m
    echo "Additional worker $i started."
    # Adjust sleep time as needed based on your system's initialization time
#    sleep 0
done

# Return to the project's root directory (assuming the npm project is there)
cd ..

# Run npm start as a background process and log output
npm start > $NPM_LOG 2>&1 &
echo "NPM project started."

# The sleep 2 is intended to give npm start some time to initialize before any other commands might be run
sleep 2

# Optionally return to the last directory, useful if this script is run from the project root
cd -
