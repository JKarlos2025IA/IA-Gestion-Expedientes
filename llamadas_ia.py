# -*- coding: utf-8 -*-
import os
import requests
import json
from config import CLAUDE_API_KEY  # AsegÃºrate de que estÃ¡ importado correctamente

# Verificar si la API key estÃ¡ definida correctamente
if not CLAUDE_API_KEY or CLAUDE_API_KEY == "CLAVE_NO_ENCONTRADA":
    print("âš ï¸ ERROR: La clave de API de Claude no estÃ¡ configurada correctamente.")
else:
    print(f"âœ… Claude API Key detectada: {CLAUDE_API_KEY[:10]}********")

# FunciÃ³n para hacer la llamada a la API de Claude
def consulta_claude(mensaje):
    url = "https://api.anthropic.com/v1/messages"  # URL de la API
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": "claude-3-7-sonnet-20250219",  # Modelo correcto
        "max_tokens": 300,
        "messages": [{"role": "user", "content": mensaje}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()

        if response.status_code == 200:
            contenido = response_json.get("content")
            if contenido:
                return contenido
            else:
                return "âš ï¸ La API no devolviÃ³ contenido en la respuesta."
        else:
            return f"âŒ Error en la consulta: {response_json.get('error', 'Error desconocido')}"

    except requests.exceptions.RequestException as e:
        return f"ðŸš¨ Error en la conexiÃ³n con la API: {str(e)}"
