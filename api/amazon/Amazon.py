



def list_contact_flows(client, InstanceId, ContactFlowTypes, NextToken, MaxResults):
    response = client.list_contact_flows(InstanceId = InstanceId, ContactFlowTypes = ContactFlowTypes, NextToken = NextToken, MaxResults = MaxResults)
    return response

def describe_contact(client, InstanceId, ContactId):
    response = client.describe_contact(InstanceId = InstanceId, ContactId = ContactId)
    return response