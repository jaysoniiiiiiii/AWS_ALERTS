import requests
import json
# from app import db
from .models import AccountInfo

from features.models import db, AccountInfo

user = AccountInfo.query.all()


username = user.email
print(username)
api_url = f'https://api.github.com/users/{username}'
repo_url = f'https://api.github.com/users/{username}/repos'

response = requests.get(api_url)
profile_data = response.json()

response = requests.get(repo_url)
repositories_data = response.json()

profile = {
    'name': profile_data.get('name', ''),
    'username': profile_data.get('login', ''),
    'bio': profile_data.get('bio', ''),
    'location': profile_data.get('location', ''),
    'join_date': profile_data.get('created_at', ''),
    "followers": profile_data.get('followers', ''),
  "following": profile_data.get('following', ''),
  "public repositories": profile_data.get('public_repos', '')
}

repositories = []
for repo in repositories_data:
    repositories.append({
        'name': repo['name'],
        'language': repo['language'],
        'stars': repo['stargazers_count'],
        'watchers count' : repo['watchers_count'],
        'open issues count' : repo['open_issues_count'],
        'created at' : repo['created_at'],
        'updated at' : repo['updated_at'],
        'pushed at' : repo['pushed_at'],
        'url' : repo['clone_url'],
    })

user_data = {'profile': profile, 'repositories': repositories}

output_filename = f"{username}_profile.json"
with open(output_filename, 'w') as json_file:
    json.dump(user_data, json_file, indent=4)

print(f"User profile data saved to {output_filename}")