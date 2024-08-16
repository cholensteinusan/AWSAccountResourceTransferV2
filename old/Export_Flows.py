import json
import aiobotocore
import asyncio
import Settings as Settings
import os

# Get the current directory where the Python script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Move the downloads directory one level up
parent_dir = os.path.dirname(current_dir)
downloads_dir = os.path.join(parent_dir, "downloads")
flows_dir = os.path.join(downloads_dir, "flows")
# Create the "downloads" directory if it doesn't exist
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

async def create_client():
    session = aiobotocore.get_session()
    source_instance_id = Settings.SOURCE_INSTANCE_ARN
    async with session.create_client(
        'connect', 
        region_name=Settings.SOURCE_REGION,
        aws_access_key_id=Settings.SOURCE_ACCESS_KEY,
        aws_secret_access_key=Settings.SOURCE_SECRET_KEY,
        aws_session_token=Settings.SOURCE_SESSION_TOKEN
    ) as client:
        return client, source_instance_id

# Download flows
async def download_flows():
    if not os.path.exists(flows_dir):
        os.makedirs(flows_dir)
    print('downloading flows')
    source_client, source_instance_id = await create_client()
    response = await source_client.list_contact_flows(
        InstanceId=source_instance_id,
        ContactFlowTypes=[
            'CONTACT_FLOW', 'CUSTOMER_QUEUE', 'CUSTOMER_HOLD', 'CUSTOMER_WHISPER', 
            'AGENT_HOLD', 'AGENT_WHISPER', 'OUTBOUND_WHISPER', 'AGENT_TRANSFER', 'QUEUE_TRANSFER'
        ],
        MaxResults=1000
    )
    print('downloaded flows resp: ', response)
    await save_flows(source_client, source_instance_id, response)

# Save flows
async def save_flows(source_client, source_instance_id, response):
    for flow in response['ContactFlowSummaryList']:
        if flow['ContactFlowState'] == 'ACTIVE':
            try:
                descResponse = await source_client.describe_contact_flow(
                    InstanceId=source_instance_id,
                    ContactFlowId=flow['Id']
                )
                file_path = os.path.join(flows_dir, f"{flow['Name']}.json")
                with open(file_path, "w") as f:
                    f.write(json.dumps(descResponse))
                await asyncio.sleep(0.15)
            except Exception as e:
                print("Exception: ", e)

# Download queues
async def download_queues():
    print('downloading queues')
    source_client, source_instance_id = await create_client()
    response = await source_client.list_queues(
        InstanceId=source_instance_id,
        QueueTypes=['STANDARD'],
        MaxResults=1000
    )
    file_path = os.path.join(downloads_dir, "Queues.json")
    with open(file_path, "w") as f:
        f.write(json.dumps(response))
    print('downloaded queues resp: ', response)

"""
# Example usage
async def main():
    await download_flows()
    await download_queues()

# Run the main function
asyncio.run(main())
"""
