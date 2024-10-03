import boto3
import boto3.session
import sys
import csv
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import app_settings as Settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from api.amazon.Amazon import list_hours_of_operations, describe_hours_of_operation

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

def download_hoop():
    source_client, source_instance_id = create_client()
    returnStatus = {
         'statusCode': '200',
         'statusResponse': 'GOOD'
    }
    try:
        response = list_hours_of_operations(source_client, source_instance_id, 1000)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            returnStatus['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
            returnStatus['statusResponse'] = 'FAILED'
            return returnStatus
        hours_of_operations = response['HoursOfOperationSummaryList']
        hoop_dir = os.path.join(Settings.settings['DOWNLOADS_PATH'], 'hours')
        if not os.path.exists(hoop_dir):
            os.makedirs(hoop_dir)
        csv_file = os.path.join(hoop_dir, 'amazon_hours_of_operation.csv')
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Name', 'Id', 'Description', 'TimeZone', 'Config'])

            for hours in hours_of_operations:
                # Describe each hours of operation
                details = describe_hours_of_operation(source_client, source_instance_id, hours['Id'])
                hours_details = details['HoursOfOperation']
                
                # Write the details to the CSV file
                writer.writerow([
                    hours_details['Name'],
                    hours_details['HoursOfOperationId'],
                    hours_details.get('Description', ''),
                    hours_details['TimeZone'],
                    hours_details['Config']
                ])
    except Exception as e:
        print(f"An error occurred: {e}")
        returnStatus['statusCode'] = '500'
        returnStatus['statusResponse'] = 'FAILED'
        returnStatus['exception'] = str({e})
    return returnStatus