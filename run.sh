#!/bin/bash
# Simple run script

if [ "$1" = "server" ]; then
    echo "Starting server on http://localhost:5000"
    python3 server.py
elif [ "$1" = "cli" ]; then
    echo "Starting CLI client"
    python3 cli_client.py
else
    echo "Usage:"
    echo "  ./run.sh server    # Start API server"
    echo "  ./run.sh cli       # Start CLI client"
fi
