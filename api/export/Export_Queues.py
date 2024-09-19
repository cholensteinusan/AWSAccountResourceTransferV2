# Download queues
def download_queues(client, instance_id):
    response = client.list_queues(
        InstanceId=instance_id,
        QueueTypes=['STANDARD'],
        MaxResults=1000
    )
    file_path = os.path.join(downloads_dir, "Queues.json")
    with open(file_path, "w") as f:
        f.write(json.dumps(response))