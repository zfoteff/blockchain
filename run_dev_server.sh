#!/bin/bash
# Author: Zac Foteff
# Version: 1.0.0

echo "[---] Starting server . . ."

uvicorn server:app --host 0.0.0.0 --port 8080