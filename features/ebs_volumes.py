import boto3
from features.models import AccountInfo
from flask import Blueprint, render_template, session, redirect, url_for

def get_ebs_volumes(aws_access_key_id, aws_secret_access_key, aws_session_token=None, region_name=None):
    print("AWS Access Key ID:", aws_access_key_id)
    print("AWS Secret Access Key:", aws_secret_access_key)
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )
    ec2_client = session.client('ec2')
    ebs_volume_list = []

    response = ec2_client.describe_volumes()

    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        volume_type = volume['VolumeType']
        size_gb = volume['Size']
        availability_zone = volume['AvailabilityZone']
        create_time = volume['CreateTime'].strftime('%Y-%m-%d %H:%M:%S')
        state = volume['State']

        ebs_volume_list.append({
            "Volume ID": volume_id,
            "Type": volume_type,
            "Size (GB)": size_gb,
            "Availability Zone": availability_zone,
            "Create Time": create_time,
            "State": state
        })

    print(ebs_volume_list)

    return ebs_volume_list

if __name__ == "__main__":
    # Replace these with your AWS credentials
    user_id = session['user_id']
    user = AccountInfo.query.get(user_id)
    aws_access_key_id = user.accesskey
    aws_secret_access_key = user.secreteaccesskey
    # aws_session_token = 'YOUR_SESSION_TOKEN'  # If using temporary credentials
    region_name = 'us-west-2'  # Replace with your region

    volumes = get_ebs_volumes(aws_access_key_id, aws_secret_access_key, region_name=region_name)
    for volume in volumes:
        print(volume)
