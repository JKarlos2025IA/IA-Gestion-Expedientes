import requests
import os

API_KEY = os.environ.get("CLAUDE_API_KEY", "CLAVE_NO_ENCONTRADA")

url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": API_KEY,
    "content-type": "application/json",
    "anthropic-version": "2023-06-01"
}

data = {
    "model": "claude-3-7-sonnet-20250219",
    "max_tokens": 300,
    "messages": [{"role": "user", "content": "Hola, cómo estás?"}]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
