


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