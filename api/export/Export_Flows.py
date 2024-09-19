import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import app_settings as Settings

import json
import boto3
import time

# Get the current directory where the Python script is located
'''current_dir = os.path.dirname(os.path.abspath(__file__))

# Move the downloads directory one level up
parent_dir = os.path.dirname(current_dir)
downloads_dir = os.path.join(parent_dir, "downloads")
flows_dir = os.path.join(downloads_dir, "flows")

# Create the "downloads" directory if it doesn't exist
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)'''

def create_client():
    source_instance_id = Settings.settings['SOURCE_INSTANCE_ID']
    source_client = boto3.client(
        'connect', 
        region_name=Settings.settings['SOURCE_REGION'],
        aws_access_key_id=Settings.settings['SOURCE_ACCESS_KEY'],
        aws_secret_access_key=Settings.settings['SOURCE_SECRET_KEY'],
        aws_session_token=Settings.settings['SOURCE_SESSION_TOKEN']
    )
    return source_client, source_instance_id

def download_flows():
    #if not os.path.exists(flows_dir):
     #   os.makedirs(flows_dir)
    print('downloading flows')
    source_client, source_instance_id = create_client()
    try:
        response = source_client.list_contact_flows(
            InstanceId=source_instance_id,
            ContactFlowTypes=[
                'CONTACT_FLOW', 'CUSTOMER_QUEUE', 'CUSTOMER_HOLD', 'CUSTOMER_WHISPER', 
                'AGENT_HOLD', 'AGENT_WHISPER', 'OUTBOUND_WHISPER', 'AGENT_TRANSFER', 'QUEUE_TRANSFER'
            ],
            MaxResults=1000
        )
    except Exception as e:
        print(f'Exception occurred: {e}')
        return None
    print('downloaded flows resp: ', response)
    save_flows(source_client, source_instance_id, response)
    return response

def save_flows(source_client, source_instance_id, response):
    for flow in response['ContactFlowSummaryList']:
        if flow['ContactFlowState'] == 'ACTIVE':
            try:
                descResponse = source_client.describe_contact_flow(
                    InstanceId=source_instance_id,
                    ContactFlowId=flow['Id']
                )
                file_path = os.path.join(flows_dir, f"{flow['Name']}.json")
                with open(file_path, "w") as f:
                    f.write(json.dumps(descResponse))
                time.sleep(0.15)
            except Exception as e:
                print("Exception: ", e)

if __name__ == "__main__":
    download_flows()
