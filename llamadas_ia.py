import requests
import json
from config import CLAUDE_API_KEY

print("Usando API Key:", CLAUDE_API_KEY)

# Función para hacer la llamada a la API de Claude
def consulta_claude(mensaje):
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "claude-3-opus-2024-02-29",
        "prompt": mensaje,
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("completion", "⚠️ No se recibió respuesta.")
    else:
        return f"⚠️ Error en la consulta: {response.text}"

