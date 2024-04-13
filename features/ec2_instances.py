import boto3
from features.models import AccountInfo
from flask import Blueprint, render_template, session, redirect, url_for


def get_ec2_instances(aws_access_key_id, aws_secret_access_key, aws_session_token=None, region_name=None):
    print("AWS Access Key ID:", aws_access_key_id)
    print("AWS Secret Access Key:", aws_secret_access_key)
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )
    client = session.client('ec2')
    EC2_instance_list = []
    response = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped', 'running']}])

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            key_name = instance.get('KeyName', 'N/A')
            private_ip_address = instance.get('PrivateIpAddress', 'N/A')
            public_ip_address = instance.get('PublicIpAddress', 'N/A')
            launch_time = instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')

            # Retrieve the instance name from tags
            instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')

            EC2_instance_list.append({
                "EC2 Instance ID": instance_id,
                "Name": instance_name,
                "State": instance['State']['Name'],
                "Type": instance_type,
                "Key Name": key_name,
                "Private IP": private_ip_address,
                "Public IP": public_ip_address,
                "Launch Time": launch_time
            })
    print(EC2_instance_list)

    return EC2_instance_list

if __name__ == "__main__":
    # Replace these with your AWS credentials
    user_id = session['user_id']
    user = AccountInfo.query.get(user_id)
    aws_access_key_id = user.accesskey
    aws_secret_access_key = user.secreteaccesskey
    # aws_session_token = 'YOUR_SESSION_TOKEN'  # If using temporary credentials
    region_name = 'us-west-2'  # Replace with your region

    instances = get_ec2_instances(aws_access_key_id, aws_secret_access_key, region_name=region_name)
    for instance in instances:
        print(instance)
