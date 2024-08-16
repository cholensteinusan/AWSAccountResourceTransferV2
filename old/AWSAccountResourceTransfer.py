#Must increase Queue limit quota

#list all routing profiles and put them into a list
#go through each iteration of the list and list routing profile queues
#then create a new destination client - describe the queues and get queue names
#describe each of the queue names to get queue arn

#api calls:
#(src)list routing profiles
#(src)describe routing profile
#(src)list routing profile queues
#(desination) describe queue 
#(destination) create routing profile 
import os
import boto3

source_access_key = ''
source_secret_key = ''
source_session_token = ''
destination_access_key = ''
destination_secret_key = ''
destination_session_token = ''


source_client = boto3.client(
    'connect', 
    region_name='us-east-1',
    aws_access_key_id = source_access_key,
    aws_secret_access_key=source_secret_key,
    aws_session_token=source_session_token
)
destination_client = boto3.client(
    'connect', 
    region_name='us-east-1',
    aws_access_key_id=destination_access_key,
    aws_secret_access_key=destination_secret_key,
    aws_session_token=destination_session_token
)

source_instance_id = '42d6a67e-fa84-47c2-a1ba-03820c48e5d6' #currently set to ps dev
destination_instance_id = 'c77b5ada-3f83-42b6-8b26-0513cfdaf264' # my personal acct


#Hours of operation start
#get the hours of operation
def list_hours_of_operation(client, instance_id):
    hoursOfOperationIds = []
    hoursOfOperationArns = []
    try:
        response = client.list_hours_of_operations(InstanceId=instance_id, MaxResults=1000)
        for hours in response['HoursOfOperationSummaryList']:
            hoursOfOperationIds.append(hours['Id'])
            hoursOfOperationArns.append(hours['Arn'])
        print("List hours of operation list: ", hoursOfOperationIds)
        return hoursOfOperationIds, hoursOfOperationArns
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
hoursOfOperationName = ''
hoursOfOperationDescription = ''
hoursOfOperationTZ = ''
hoursOfOperationTags = ''
hoursOfOperationConfig = ''


#describe the current hours of operation from the list
def describe_hours_of_operation(client, instance_id, hoursID):
    global hoursOfOperationName, hoursOfOperationDescription, hoursOfOperationTZ, hoursOfOperationTZ, hoursOfOperationTags, hoursOfOperationConfig
    try:
        response = client.describe_hours_of_operation(InstanceId=instance_id, HoursOfOperationId=hoursID)
        hoursOfOperationName = response['HoursOfOperation']['Name']
        hoursOfOperationDescription = response['HoursOfOperation']['Description']
        hoursOfOperationTZ = response['HoursOfOperation']['TimeZone']
        hoursOfOperationTags = response['HoursOfOperation']['Tags']
        hoursOfOperationConfig = response['HoursOfOperation']['Config']
        print("Describe hours is describing: ",hoursOfOperationName, hoursOfOperationTZ)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


#create hours of operation
def create_hours_of_operation(client, instance_id):
    try:
        response = client.create_hours_of_operation(InstanceId=instance_id, Name=hoursOfOperationName, 
                                                    Description=hoursOfOperationDescription, TimeZone=hoursOfOperationTZ, 
                                                    Config=hoursOfOperationConfig, Tags=hoursOfOperationTags)
        print("Create hours of operation ARN ID: ",response['HoursOfOperationArn'])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
#end hours of operation

#begin queues
def list_queues(client, instance_id):
    paginator = client.get_paginator('list_queues')
    page_iterator = paginator.paginate(InstanceId=instance_id)
    queue_ids = []
    for page in page_iterator:
        for queue in page['QueueSummaryList']:
            if queue['QueueType'] == 'STANDARD':
                queue_ids.append(queue['Id'])
    return queue_ids

def describe_queue(client, instance_id, queue_id):
    try:
        response = client.describe_queue(InstanceId=instance_id, QueueId=queue_id)
        queue_config = response['Queue']
        # Extract only the OutboundCallerIdName
        outbound_caller_id_name = queue_config.get('OutboundCallerConfig', {}).get('OutboundCallerIdName', None)
        queue_config['OutboundCallerIdName'] = outbound_caller_id_name
        return queue_config
    except client.exceptions.ResourceNotFoundException:
        print(f"Queue not found: {queue_id} in instance {instance_id}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def create_queue(client, instance_id, queue_config, hours_mapping):
    # Map Hours of Operation ID
    original_hours_id = queue_config['HoursOfOperationId']
    new_hours_id = hours_mapping.get(original_hours_id, None)
    if not new_hours_id:
        print(f"Missing new Hours of Operation ID for original ID: {original_hours_id}. Skipping queue {queue_config['Name']}.")
        return

    # Initialize OutboundCallerConfig dictionary
    outbound_caller_config = {}
    if 'OutboundCallerIdName' in queue_config and queue_config['OutboundCallerIdName']:
        outbound_caller_config['OutboundCallerIdName'] = queue_config['OutboundCallerIdName']

    try:
        request_params = {
            'InstanceId': instance_id,
            'Name': queue_config['Name'],
            'Description': queue_config.get('Description', ''),
            'HoursOfOperationId': new_hours_id
        }

        if outbound_caller_config:
            request_params['OutboundCallerConfig'] = outbound_caller_config

        response = client.create_queue(**request_params)
        print(f"Queue {queue_config['Name']} created successfully.")
    except client.exceptions.ResourceNotFoundException:
        print(f"Resource not found when trying to create queue {queue_config['Name']}. Check dependent resource configurations.")
    except client.exceptions.DuplicateResourceException:
        print(f"Skipping creation: A queue named {queue_config['Name']} already exists.")
    except Exception as e:
        print(f"Failed to create queue {queue_config['Name']}: {str(e)}")
#end queues

#begin routing profiles
# get all routing profiles in a list
def list_routing_profiles(client, instance_id):
    routing_profiles = []
    routing_profiles_names = []
    paginator = client.get_paginator('list_routing_profiles')
    page_iterator = paginator.paginate(InstanceId=instance_id)
    try:
        for page in page_iterator:
            for rp in page['RoutingProfileSummaryList']:
                routing_profiles.append(rp['Id'])
                routing_profiles_names.append(rp['Name'])
        print("Routing profiles: ",routing_profiles)
        return routing_profiles, routing_profiles_names
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Describe each routing profile so we can get the top level data
# Source Acct
rp_name = ''
rp_queue_amount = ''
rp_user_amt = ''
rp_queue_amt = ''
rp_description = ''
rp_associatedQueues = []
rp_channels = []
rp_concurrency = []
rp_default_outbound_queue = ''
rp_cross_channel_behavior = []
rp_media_concurrenciesList = []
rp_describe_source_mediaConcurrenciesDict = {
    "Channel": "",
    "Concurrency": 0,
    "CrossChannelBehaviour": {
        "BehaviorType": ""
    }
}
def describe_routing_profile(client, instance_id, routing_profile_id):
    global rp_queue_amount, rp_user_amt, rp_queue_amt, rp_description, rp_name, rp_default_outbound_queue
    try:
        response = client.describe_routing_profile(InstanceId = instance_id, RoutingProfileId = routing_profile_id)
        rp_name = response['RoutingProfile']['Name']
        rp_queue_amount = response['RoutingProfile']['NumberOfAssociatedQueues']
        rp_user_amt = response['RoutingProfile']['NumberOfAssociatedUsers']
        rp_queue_amt = response['RoutingProfile']['NumberOfAssociatedQueues']
        rp_description = response['RoutingProfile']['Description']
        rp_default_outbound_queue = response['RoutingProfile']['DefaultOutboundQueueId']
        print('Describing Routing profile: ', rp_name)
        source_describe_queue_rp(source_client, source_instance_id, rp_default_outbound_queue)
        for i in range(len(response['RoutingProfile']['MediaConcurrencies'])):
            if (response['RoutingProfile']['MediaConcurrencies'][i]['Channel']):
                rp_describe_source_mediaConcurrenciesDict['Channel'] = response['RoutingProfile']['MediaConcurrencies'][i]['Channel']
                rp_describe_source_mediaConcurrenciesDict['Concurrency'] = response['RoutingProfile']['MediaConcurrencies'][i]['Concurrency']
                rp_describe_source_mediaConcurrenciesDict['CrossChannelBehaviour']['BehaviorType'] = response['RoutingProfile']['MediaConcurrencies'][i]['CrossChannelBehavior']['BehaviorType']
                rp_media_concurrenciesList.append(rp_describe_source_mediaConcurrenciesDict)
    except client.exceptions.ResourceNotFoundException:
        print(f"routing profile not found: {routing_profile_id} in instance {instance_id}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# we need to get the queue ID for the singular outbound queue ID... unfortunately this simple thing takes two api calls
# pass in rp_default_outbound_queue for outbound_queueId
rp_outbound_queueName_Src = ''
def source_describe_queue_rp(client, instance_id, outbound_queueId):
    global rp_outbound_queueName_Src
    response = client.describe_queue(InstanceId = instance_id, QueueId = outbound_queueId)
    rp_outbound_queueName_Src = response['Queue']['Name']
    print("source queue described: ",rp_outbound_queueName_Src)

# Now we have the outbound queue name from the source acct, we need to get the ID of this singular queue 
rp_outbound_queueId_Dst = ''
def list_queues_outboundQueue(client, instance_id):
    global rp_outbound_queueId_Dst
    response = client.list_queues(InstanceId = instance_id, QueueTypes=['STANDARD'], MaxResults=1000)
    for queueSummary in response['QueueSummaryList']:
            if queueSummary['Name'] == rp_outbound_queueName_Src:
                rp_outbound_queueId_Dst =  queueSummary["Id"]
                print("destination queue id for outbound queue: ",rp_outbound_queueId_Dst)
                
# We must then get the queue data, mainly the names, we need the queue name so we can get the Queue ID from our destination account
#rp_queue_Ids = []
rp_queue_names = []
rp_queue_priority = []
rp_queue_delay = []
def list_routing_profile_queues(client, instance_id, routing_profile_id):
    response = client.list_routing_profile_queues(InstanceId = instance_id, RoutingProfileId = routing_profile_id)
    #print("Listing routing profile queue: ", response)
    for i in range(len(response['RoutingProfileQueueConfigSummaryList'])):
        if (response['RoutingProfileQueueConfigSummaryList'][i]['QueueName']):
             rp_queue_names.append(response['RoutingProfileQueueConfigSummaryList'][i]['QueueName'])
            #rp_queue_Ids.append(response['QueueId'])
            # rp_queue_priority.append(response['RoutingProfileQuueConfigSummaryList'][i]['Priority'])
           #  rp_queue_delay.append(response['RoutingProfileQueueConfigSummaryList'][i]['Delay'])
           #  print(response['RoutingProfileQueueConfigSummaryList '][i]['QueueName'])
    print(rp_queue_names)

#end routing profiles
#begin operations
source_hoursOfOperationIds = []
def copy_hours_of_operation():
    #hours of operation
    global source_hoursOfOperationIds
    source_hoursOfOperationIds, source_hoursOfOperationArns = list_hours_of_operation(source_client, source_instance_id)
    hoursOfOperationLength = len(source_hoursOfOperationIds)
    for index in range(hoursOfOperationLength):
        describe_hours_of_operation(source_client, source_instance_id, source_hoursOfOperationIds[index])
        create_hours_of_operation(destination_client, destination_instance_id)
    print("end of hours of operation")
    #end hours of operation

destination_hoursOfOperationIds = []
def copy_queues(source_client, destination_client, source_instance_id, destination_instance_id):
    global destination_hoursOfOperationIds
    destination_hoursOfOperationIds, destination_hoursOfOperationArns = list_hours_of_operation(destination_client, destination_instance_id)
    hours_mapping = dict(zip(source_hoursOfOperationIds, destination_hoursOfOperationIds))
    print(hours_mapping)
    queue_ids = list_queues(source_client, source_instance_id)
    print(queue_ids)
    for queue_id in queue_ids:
            queue_config = describe_queue(source_client, source_instance_id, queue_id)
            if queue_config is not None:  # Ensure queue_config is not None before proceeding
                # Pass the hours_mapping to the create_queue function
                create_queue(destination_client, destination_instance_id, queue_config, hours_mapping)
                print(f"Queue {queue_config['Name']} processed.")
            else:
                print(f"Failed to retrieve configuration for queue ID {queue_id}.")

def copy_routing_profiles():
    source_routing_profile, source_routing_profile_names = list_routing_profiles(source_client, source_instance_id)
    rp_length = len(source_routing_profile)
    print(rp_length)
    for index in range(rp_length):
        describe_routing_profile(source_client, source_instance_id, source_routing_profile[index])
        list_queues_outboundQueue(destination_client, destination_instance_id)
        list_routing_profile_queues(source_client, source_instance_id, source_routing_profile[index])

#end operations


def main():
    #copy_hours_of_operation()
    #copy_queues(source_client, destination_client, source_instance_id, destination_instance_id)
    copy_routing_profiles()
    

main()