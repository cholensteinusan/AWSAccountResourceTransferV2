


#connect
def list_contact_flows(client, InstanceId, ContactFlowTypes, NextToken, MaxResults):
    response = client.list_contact_flows(InstanceId = InstanceId, ContactFlowTypes = ContactFlowTypes, NextToken = NextToken, MaxResults = MaxResults)
    return response

def list_contact_flow_modules(client, InstanceId, ContactFlowModuleState, NextToken, MaxResults):
    response = client.list_contact_flow_modules(InstanceId = InstanceId, ContactFlowModuleState = ContactFlowModuleState, NextToken = NextToken, MaxResults = MaxResults)
    return response

def describe_contact_flow(client, InstanceId, ContactFlowId):
    response = client.describe_contact_flow(InstanceId = InstanceId, ContactFlowId = ContactFlowId)
    return response

def describe_contact_flow_module(client, InstanceId, ContactFlowModuleId):
    response = client.describe_contact_flow_module(InstanceId = InstanceId, ContactFlowModuleId = ContactFlowModuleId)
    return response

'''def list_bots(client, InstanceId, NextToken, MaxResults, LexVersion):
    response = client.list_bots(InstanceId = InstanceId, NextToken = NextToken, MaxResults = MaxResults, LexVersion = LexVersion)
    return response'''

def list_queues(client, InstanceId, QueueTypes, NextToken, MaxResults):
    response = client.list_queues(InstanceId = InstanceId, QueueTypes = QueueTypes, NextToken = NextToken, MaxResults = MaxResults)
    return response

def list_queues(client, InstanceId, QueueTypes, MaxResults):
    response = client.list_queues(InstanceId = InstanceId, QueueTypes = QueueTypes, MaxResults = MaxResults)
    return response

def list_hours_of_operations(client, InstanceId, NextToken, MaxResults):
    response = client.list_hours_of_operations(InstanceId = InstanceId, NextToken = NextToken, MaxResults = MaxResults)
    return response

def list_hours_of_operations(client, InstanceId, MaxResults):
    response = client.list_hours_of_operations(InstanceId = InstanceId, MaxResults = MaxResults)
    return response

def describe_hours_of_operation(client, InstanceId, HoursOfOperationId):
    response = client.describe_hours_of_operation(InstanceId = InstanceId, HoursOfOperationId = HoursOfOperationId)
    return response

#lex
def list_bots(client, sortBy, filters, maxResults, nextToken):
    response = client.list_bots(sortBy = sortBy, filters = filters, maxResults = maxResults, nextToken = nextToken)
    return response

def list_bots(client, sortBy, filters, maxResults):
    response = client.list_bots(sortBy = sortBy, filters = filters, maxResults = maxResults)
    return response

def list_bots(client, maxResults):
    response = client.list_bots(maxResults = maxResults)
    return response

def list_bot_versions(client, botId, sortBy, maxResults, nextToken):
    response = client.list_bot_versions(botId = botId, sortBy = sortBy, maxResults = maxResults, nextToken = nextToken)
    return response

def list_bot_versions(client, botId, sortBy, maxResults):
    response = client.list_bot_versions(botId = botId, sortBy = sortBy, maxResults = maxResults)
    return response

def create_export(client, resourceSpecification, fileFormat, filePassword):
    response = client.create_export(resourceSpecification = resourceSpecification, fileFormat = fileFormat, filePassword = filePassword)
    return response

def create_export(client, resourceSpecification, fileFormat):
    response = client.create_export(resourceSpecification = resourceSpecification, fileFormat = fileFormat)
    return response

def describe_export(client, exportId):
    response = client.describe_export(exportId = exportId)
    return response