#!/usr/bin/env python3
import requests

url = "https://telex-discord-integration.onrender.com/telex-webhook"  # Change to your FastAPI endpoint
payload = {
    "content": "Hello, Team Baydre Africa!"  # Ensure the payload includes the 'content' field
}

response = requests.post(
    url,
    json=payload,
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
)
print(response.json())