import os

# Obtener claves desde variables de entorno
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "CLAVE_NO_ENCONTRADA")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "CLAVE_NO_ENCONTRADA")
print("Claude API Key:", os.getenv("CLAUDE_API_KEY"))
print("Gemini API Key:", os.getenv("GEMINI_API_KEY"))

# Configurar las claves de API
APIS_DISPONIBLES = {
    "Claude": {
        "nombre": "Claude (Anthropic)",
        "clave": CLAUDE_API_KEY,
        "url": "https://api.anthropic.com/v1/complete",
        "modelo": "claude-3-opus-2024-02-29"
    },
    "Gemini": {
        "nombre": "Gemini (Google)",
        "clave": GEMINI_API_KEY,
        "url": "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        "modelo": "gemini-pro"
    }
}
# Función para obtener la API seleccionada
def obtener_api(nombre_api):
    return APIS_DISPONIBLES.get(nombre_api, None)

def consulta_claude(mensaje):
    try:
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
    except Exception as e:
        return f"⚠️ Error inesperado: {str(e)}"


