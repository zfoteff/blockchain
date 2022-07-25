#!/bin/bash
# Author: Zac Foteff
# Version: 1.0.0
#
# Start the server. has options to clear the logs and

echo "[---] Clearing Logs . . ."
# Clear logs: rm logs/*
echo "[---] Starting server . . ."
uvicorn server:app --host 0.0.0.0 --port 8080