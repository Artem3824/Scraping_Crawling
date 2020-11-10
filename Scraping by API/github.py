import requests
import json
from pprint import pprint

user = 'artem3824'
response = requests.get(f'https://api.github.com/users/{user}/repos')
# print(response)
if response.ok:
    data = json.loads(response.text)
    with open(f'github_repos_{user}.json', 'w') as f:
        json.dump(data, f)

    for repo in data:
        print(repo['name'])
