import requests
import os

API_KEY = os.getenv("CLAUDE_API_KEY")
url = "https://api.anthropic.com/v1/messages"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "claude-3-7-sonnet-20250219",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hola"}]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())


