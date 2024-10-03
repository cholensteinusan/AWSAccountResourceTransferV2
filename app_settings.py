# app_settings.py
import os
from pathlib import Path
APPLICATION_NAME = 'AWS Account Utilities'

settings = {
    'DOWNLOADS_PATH': Path.home() / "Downloads",
    'SOURCE_ACCESS_KEY': '',
    'SOURCE_SECRET_KEY': '',
    'SOURCE_SESSION_TOKEN': '',
    'SOURCE_INSTANCE_ID': '',
    'SOURCE_REGION': '',
    'DESTINATION_ACCESS_KEY': '',
    'DESTINATION_SECRET_KEY': '',
    'DESTINATION_SESSION_TOKEN': '',
    'DESTINATION_INSTANCE_ID': '',
    'DESTINATION_REGION': ''
}
