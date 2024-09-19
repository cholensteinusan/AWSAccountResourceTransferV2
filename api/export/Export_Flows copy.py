import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import app_settings as Settings

import json
import boto3
import time

# Get the current directory where the Python script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Move the downloads directory one level up
parent_dir = os.path.dirname(current_dir)
downloads_dir = os.path.join(parent_dir, "downloads")
flows_dir = os.path.join(downloads_dir, "flows")

# Create the "downloads" directory if it doesn't exist
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

