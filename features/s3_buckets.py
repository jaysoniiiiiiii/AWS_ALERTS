import boto3
from features.models import AccountInfo
from flask import Blueprint, render_template, session, redirect, url_for

def get_s3_buckets(aws_access_key_id, aws_secret_access_key, aws_session_token=None, region_name=None):
    print("AWS Access Key ID:", aws_access_key_id)
    print("AWS Secret Access Key:", aws_secret_access_key)
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )
    s3_client = session.client('s3')
    s3_bucket_list = []

    response = s3_client.list_buckets()

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')

        # Optionally, you can list objects within each bucket
        # response = s3_client.list_objects_v2(Bucket=bucket_name)
        # objects = response.get('Contents', [])
        # object_count = len(objects)

        s3_bucket_list.append({
            "Bucket Name": bucket_name,
            "Creation Date": creation_date,
            # "Object Count": object_count  # Uncomment this line to include object count
        })

    # print(s3_bucket_list)

    return s3_bucket_list

if __name__ == "__main__":
    # Replace these with your AWS credentials
    user_id = session['user_id']
    user = AccountInfo.query.get(user_id)
    aws_access_key_id = user.accesskey
    aws_secret_access_key = user.secreteaccesskey
    # aws_session_token = 'YOUR_SESSION_TOKEN'  # If using temporary credentials
    region_name = 'us-west-2'  # Replace with your region

    buckets = get_s3_buckets(aws_access_key_id, aws_secret_access_key, region_name=region_name)
    # for bucket in buckets:
    #     print(bucket)
