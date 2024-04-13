import boto3
from features.models import AccountInfo
from flask import Blueprint, render_template, session, redirect, url_for

def get_eks_clusters(aws_access_key_id, aws_secret_access_key, aws_session_token=None, region_name=None):
    print("AWS Access Key ID:", aws_access_key_id)
    print("AWS Secret Access Key:", aws_secret_access_key)
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )
    eks_client = session.client('eks')
    eks_cluster_list = []

    response = eks_client.list_clusters()

    for cluster_name in response['clusters']:
        cluster_info = eks_client.describe_cluster(name=cluster_name)
        cluster_arn = cluster_info['cluster']['arn']
        cluster_status = cluster_info['cluster']['status']
        cluster_version = cluster_info['cluster']['version']
        create_time = cluster_info['cluster']['createdAt'].strftime('%Y-%m-%d %H:%M:%S')

        eks_cluster_list.append({
            "Cluster Name": cluster_name,
            "ARN": cluster_arn,
            "Status": cluster_status,
            "Version": cluster_version,
            "Creation Time": create_time
        })

    print(eks_cluster_list)

    return eks_cluster_list

if __name__ == "__main__":
    # Replace these with your AWS credentials
    user_id = session['user_id']
    user = AccountInfo.query.get(user_id)
    aws_access_key_id = user.accesskey
    aws_secret_access_key = user.secreteaccesskey
    # aws_session_token = 'YOUR_SESSION_TOKEN'  # If using temporary credentials
    region_name = 'us-west-2'  # Replace with your region

    clusters = get_eks_clusters(aws_access_key_id, aws_secret_access_key, region_name=region_name)
    for cluster in clusters:
        print(cluster)
