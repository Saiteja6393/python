import boto3
from datetime import datetime, timedelta

def create_ami(instance_id):
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    ami_name = f'WeeklyBackup-{instance_id}'
    response = ec2_client.create_image(
        InstanceId=instance_id,
        Name=ami_name,
        Description='Weekly backup',
        NoReboot=True  
    )
    return response['ImageId']

current_date = datetime.utcnow()
days_to_keep = 30

    # Get a list of all AMIs
amis = ec2.describe_images(Owners=['self'])['Images']

    # Loop through each AMI and check its creation date
for ami in amis:
    creation_date = ami['CreationDate']
    ami_id = ami['ImageId']

        # Convert the creation date string to a datetime object
    creation_datetime = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Calculate the age of the AMI
    age = current_date - creation_datetime

        # If the AMI is older than the specified days_to_keep, deregister it
    if age.days > days_to_keep:
        print(f"Deleting AMI: {ami_id}")
            # Deregister the AMI
        ec2.deregister_image(ImageId=ami_id)

            # Optionally, you can also delete the associated snapshots
        for block_device in ami['BlockDeviceMappings']:
            if 'Ebs' in block_device:
                snapshot_id = block_device['Ebs']['SnapshotId']
                print(f"Deleting Snapshot: {snapshot_id}")
                ec2.delete_snapshot(SnapshotId=snapshot_id)



def send_notification(subject, message):
    sns_client = boto3.client('sns', region_name='us-east-1')
    topic_arn = 'your-sns-topic-arn'
    sns_client.publish(TopicArn=topic_arn, Subject=subject, Message=message)

if __name__ == "__main__":
    cleanup_old_amis()