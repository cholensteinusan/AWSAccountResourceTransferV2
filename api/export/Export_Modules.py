import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import app_settings as Settings

import json
import boto3
import time
from api.amazon.Amazon import list_contact_flow_modules, describe_contact_flow_module


returnStatus = {
         'statusCode': '200',
         'statusResponse': 'GOOD'
}

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

def download_modules():
    source_client, source_instance_id = create_client()
    try:
        response = list_contact_flow_modules(source_client, source_instance_id, 'ACTIVE', '', 1000)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            returnStatus['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
            returnStatus['statusResponse'] = 'FAILED'
            return returnStatus
    except Exception as e:
        returnStatus['statusCode'] = '500'
        returnStatus['statusResponse'] = 'FAILED'
        returnStatus['exception'] = str({e})
        return returnStatus
    save_modules(source_client, source_instance_id, response)
    return returnStatus

def save_modules(source_client, source_instance_id, response):
    modules_dir = os.path.join(Settings.settings['DOWNLOADS_PATH'], 'modules')
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
    for flow in response['ContactFlowModulesSummaryList']:
            try:
                descResponse = describe_contact_flow_module(
                    client=source_client,
                    InstanceId=source_instance_id,
                    ContactFlowModuleId=flow['Id']
                )

                file_path = os.path.join(modules_dir, f"{flow['Name']}.json")
                with open(file_path, "w") as f:
                    f.write(json.dumps(descResponse))
                time.sleep(0.15)
            except Exception as e:
                returnStatus['statusCode'] = '500'
                returnStatus['statusResponse'] = 'FAILED'
                returnStatus['exception'] = str({e})
    return returnStatus

