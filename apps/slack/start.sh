#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run the watcher script and pass app.py as an argument
python3 watcher.py app.py
