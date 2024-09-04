#!/usr/bin/env bash

HOST="0.0.0.0"
LOGLEVEL="warning"
PORT="8000"

echo "Starting server"
python -m uvicorn --host "$HOST" instrument_registry.server:app --port "$PORT" --log-level "$LOGLEVEL"
