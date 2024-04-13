from flask import Blueprint, render_template, session, redirect, url_for, request
from features.models import AccountInfo
import requests
import json
from features.my_email_utils import send_email
from features.ec2_instances import get_ec2_instances
from features.s3_buckets import get_s3_buckets
from features.ebs_volumes import get_ebs_volumes
from features.eks_clusters import get_eks_clusters

main_routes = Blueprint('main', __name__)

@main_routes.route('/main', methods=['GET', 'POST'])
def main_page():
    # Check if user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        # Retrieve user data using user_id
        user = AccountInfo.query.get(user_id)
        if user:
            username = user.githubusername
            api_url = f'https://api.github.com/users/{username}'
            repo_url = f'https://api.github.com/users/{username}/repos'

            # Retrieve data from GitHub API
            response = requests.get(api_url)
            profile_data = response.json()

            response = requests.get(repo_url)
            repositories_data = response.json()

            # Retrieve AWS data
            aws_access_key_id = user.accesskey
            aws_secret_access_key = user.secreteaccesskey
            region_name = 'us-west-2'  # Replace with your region

            ec2_instances = get_ec2_instances(aws_access_key_id, aws_secret_access_key, region_name="ap-south-1")
            s3_buckets = get_s3_buckets(aws_access_key_id, aws_secret_access_key, region_name="ap-south-1")
            ebs_volumes = get_ebs_volumes(aws_access_key_id, aws_secret_access_key, region_name="ap-south-1")
            eks_clusters = get_eks_clusters(aws_access_key_id, aws_secret_access_key, region_name="ap-south-1")

            # Combine user data, GitHub API data, and AWS data into a dictionary
            user_data = {
                'user': user,
                'profile': profile_data,
                'repositories': repositories_data,
                'ec2_instances': ec2_instances,
                's3_buckets': s3_buckets,
                'ebs_volumes': ebs_volumes,
                'eks_clusters': eks_clusters
            }

            if request.method == 'POST':
                # Send email functionality
                block_name = request.form.get('block_name')  # Get the block name from the form data
                email_content = format_email_content(user_data, block_name)
                print("Email Content:")
                print(email_content)  # Print email content for debugging

                sender_email = "sonij5073@gmail.com"
                sender_password = "bgyr vkbt olls ogis"
                receiver_email = user.email
                subject = "AWS Data"
                send_email(sender_email, sender_password, receiver_email, subject, email_content)

                # Redirect to the same page after sending email
                return redirect(url_for('main_routes.main_page'))

            # Pass user data to the main page template
            return render_template("main.html", user_data=user_data)

    # If user is not logged in, redirect to login page
    return redirect(url_for('login.login'))


def format_email_content(user_data, block_name):
    content = f"Hello {user_data['profile'].get('name', 'N/A')}\n\n"
    if block_name == 'ec2_instances':
        content += "EC2 Instances:\n"
        for instance in user_data['ec2_instances']:
            content += f"Name: {instance['Name']}\n"
            content += f"State: {instance['State']}\n"
            content += f"Type: {instance['Type']}\n\n"
    elif block_name == 's3_buckets':
        content += "S3 Buckets:\n"
        for bucket in user_data['s3_buckets']:
            content += f"Name: {bucket['Bucket Name']}\n"
            content += f"Creation Date: {bucket['Creation Date']}\n\n"
    elif block_name == 'ebs_volumes':
        content += "EBS Volumes:\n"
        for volume in user_data['ebs_volumes']:
            content += f"ID: {volume['Volume ID']}\n"
            content += f"Type: {volume['Type']}\n"
            content += f"Size (GB): {volume['Size (GB)']}\n"
            content += f"State: {volume['State']}\n\n"
    elif block_name == 'eks_clusters':
        content += "EKS Clusters:\n"
        for cluster in user_data['eks_clusters']:
            content += f"Name: {cluster['Cluster Name']}\n"
            content += f"Status: {cluster['Status']}\n"
            content += f"Version: {cluster['Version']}\n\n"
    return content
