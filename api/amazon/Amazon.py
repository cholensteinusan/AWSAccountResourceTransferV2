


def list_contact_flows(client, InstanceId, ContactFlowTypes, NextToken, MaxResults):
    response = client.list_contact_flows(InstanceId = InstanceId, ContactFlowTypes = ContactFlowTypes, NextToken = NextToken, MaxResults = MaxResults)
    return response

def describe_contact_flow(client, InstanceId, ContactFlowId):
    response = client.describe_contact_flow(InstanceId = InstanceId, ContactFlowId = ContactFlowId)
    return response