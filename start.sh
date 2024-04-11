#!/bin/bash

# Define log file paths
FLASK_LOG="flask-backend/flask.log"
NPM_LOG="npm-start.log"

# Ensure the log files exist and are empty
> "$FLASK_LOG"
> "$NPM_LOG"

# Change directory to the Flask backend
cd flask-backend/

# Start a detached tmux session running the Flask backend and log output
# Adding unbuffered Python execution to improve real-time logging
tmux new-session -d -s my_session "source ../.venv/bin/activate && python -u app.py > ../$FLASK_LOG 2>&1"

# Ensure the shell waits for a brief moment to allow the tmux session to initialize
sleep 1

# Return to the project's root directory (assuming the npm project is there)
cd ..

# Run npm start as a background process and log output
npm start > $NPM_LOG 2>&1 &

# The sleep 2 is intended to give npm start some time to initialize before any other commands might be run
sleep 2

# Return to the last directory, useful if this script is run from the project root
cd -
