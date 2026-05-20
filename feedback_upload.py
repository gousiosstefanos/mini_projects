import os
import requests

path = "/data/feedback"
url = "http://YOUR-IP-HERE/feedback"

for filename in os.listdir(path):
    if filename.endswith(".txt"):

        full_path = os.path.join(path, filename)

        with open(full_path, 'r') as file:
            lines = file.read().splitlines()

        data = {
        "title": lines[0],
        "name": lines[1],
        "date": lines[2],
        "feedback": lines[3]
        }
        
        response = requests.post(url, json=data)

        print(response.status_code)

