import os
import requests
print("Claude API Key desde config.py:", os.environ.get("CLAUDE_API_KEY", "NO ENCONTRADA"))
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
        "url": "https://api.anthropic.com/v1/messages",
        "modelo": "claude-3-7-sonnet-20250219"
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
    # Esta función está ahora en llamadas_ia.py
    # La dejamos aquí para compatibilidad, pero llamamos a la implementación en llamadas_ia.py
    try:
        from llamadas_ia import consulta_claude as llamada_claude
        return llamada_claude(mensaje)
    except ImportError:
        # Implementación de respaldo (no debería usarse)
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "anthropic-version": "2023-06-01",
                "x-api-key": CLAUDE_API_KEY,
                "content-type": "application/json"
            }
            data = {
                "model": "claude-3-7-sonnet-20250219",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": mensaje}]
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                for item in response.json().get("content", []):
                    if item.get("type") == "text":
                        return item.get("text", "")
                return "⚠️ No se recibió respuesta."
            else:
                return f"⚠️ Error en la consulta: {response.text}"
        except Exception as e:
            return f"⚠️ Error inesperado: {str(e)}"