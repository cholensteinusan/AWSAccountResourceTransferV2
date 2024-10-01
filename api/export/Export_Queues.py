import boto3
import boto3.session
import sys
import csv
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import app_settings as Settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import serverLog as logging
from api.amazon.Amazon import list_queues

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


def download_queues():
    source_client, source_instance_id = create_client()
    returnStatus = {
         'statusCode':'200',
         'statusResponse': 'GOOD'
    }
    try:
        QueueTypes = ['STANDARD', 'AGENT']
        MaxResults = 1000
        response = list_queues(source_client, source_instance_id, QueueTypes, MaxResults)
        if (response['ResponseMetadata']['HTTPStatusCode'] != '200'):
            returnStatus['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
            return returnStatus
        logging.loggingDictionary["list_queues_Export_Queues"] = response
        queues = response['QueueSummaryList']
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        downloads_folder_path = os.path.join(parent_directory, 'downloads')
        queues_dir = os.path.join(downloads_folder_path, 'queues')
        if not os.path.exists(queues_dir):
                os.makedirs(queues_dir)
        csv_file = os.path.join(queues_dir, 'amazon_connect_queues.csv')
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['QueueId', 'Name', 'QueueArn'])

            for queue in queues:
                queue_id = queue.get('Id')
                queue_name = queue.get('Name', 'Agent')  # Provide a default value 'N/A' if 'Name' is missing
                queue_arn = queue.get('Arn')
                writer.writerow([queue_id, queue_name, queue_arn])
    except Exception as e:
        print(f"An error occurred: {e}")