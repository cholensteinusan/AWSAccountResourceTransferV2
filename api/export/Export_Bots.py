import boto3
import time
import boto3.session
import requests 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import app_settings as Settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import serverLog as logging
from api.amazon.Amazon import list_bots, list_bot_versions, create_export, describe_export

def create_client():
    source_instance_id = Settings.settings['SOURCE_INSTANCE_ID']
    source_client = boto3.client(
        'lexv2-models', 
        region_name=Settings.settings['SOURCE_REGION'],
        aws_access_key_id=Settings.settings['SOURCE_ACCESS_KEY'],
        aws_secret_access_key=Settings.settings['SOURCE_SECRET_KEY'],
        aws_session_token=Settings.settings['SOURCE_SESSION_TOKEN']
    )
    return source_client, source_instance_id


def download_bots():
    source_client, source_instance_id = create_client()
    try:
        v2botList = []
        lexResponse = list_bots(source_client, 100)

        v2botList.extend(lexResponse["botSummaries"])
        while "nextToken" in lexResponse:
            print("Getting more lex bots from Lex")
            v2botList.extend(lexResponse["botSummaries"])
        
        for bot in v2botList:
            # First, we have to get the versions for the current bot
            sortBy={
             'attribute': 'BotVersion',
             'order': 'Descending'
            }
            response = list_bot_versions(source_client, bot["botId"], sortBy, 5)
            logging.loggingDictionary["list_bot_versions_Export_Bots for ", bot["botId"]] = response
                # Check if there are any versions available

            if len(response["botVersionSummaries"]) <= 1:
                latestVersion = response["botVersionSummaries"][0]["botVersion"] #draft version
            else:
                latestVersion = response["botVersionSummaries"][1]["botVersion"] #weird shit, basically array is ordered - 0 is draft, 1 is the newest version (its stupid af)
            
            resourceSpecification = {
                'botExportSpecification': {
                    'botId': bot["botId"],
                    'botVersion': latestVersion
                }
            }
            logging.loggingDictionary["latestversion for ", bot["botId"]] = latestVersion
            print(logging.loggingDictionary)
            fileFormat='LexJson'
            # Now we can start an export of it
            response = create_export(source_client, resourceSpecification, fileFormat)
            exportId = response["exportId"]

            # Now we get to wait around until it decides to finish
            response = describe_export(source_client, exportId)
            while response["exportStatus"] == "InProgress":
                # Take a one-second nap before asking Lex again
                time.sleep(1)
                response = describe_export(source_client, exportId)

            # Export's finished, but if status isn't Completed then spit out an error
            if response["exportStatus"] != "Completed":
                for excuse in response["failureReasons"]:
                    print("[ERROR] The export of " + bot["botName"] + " failed: " + excuse)
                continue

            # With a successful export, now we have to download it via the signedUrl
            print("Downloading signedURL for " + bot["botName"])
            downloadUrl = response["downloadUrl"]
            response = requests.get(downloadUrl, stream=True)
            parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            downloads_folder_path = os.path.join(parent_directory, 'downloads')
            lex_dir = os.path.join(downloads_folder_path, 'lex')
            if not os.path.exists(lex_dir):
                os.makedirs(lex_dir)
            with open(os.path.join(lex_dir, bot["botName"] + ".zip"), 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)
    except Exception as e:
        print(f"An error occurred: {e}")

    