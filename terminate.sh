#!/bin/bash

# Kill the Flask backend process running in the tmux session
tmux kill-session -t my_session

# Find the PID of the Node.js process running on port 3000
node_pid=$(lsof -t -i :3000)

# Check if the Node.js process is running
if [ -n "$node_pid" ]; then
  # Kill the Node.js process
  kill "$node_pid"
  echo "Node.js process running on port 3000 (PID: $node_pid) has been terminated."
else
  echo "No running Node.js process found on port 3000."
fi
