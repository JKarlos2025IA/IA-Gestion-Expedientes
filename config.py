"""
Configuración centralizada para el asistente legal
"""
import os

# API Keys para servicios de IA
CLAUDE_API_KEY = "sk-3719433fa2774b82a1c89e78575a9248"  # Clave Deepseek como alternativa
GEMINI_API_KEY = "AIzaSyABbkPcr3wTbQbmjQa3Jp7xQXkfSFg3LPI"

# Almacenar las API keys como variables de entorno para mayor seguridad
os.environ["CLAUDE_API_KEY"] = CLAUDE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Configurar las APIs disponibles
APIS_DISPONIBLES = {
    "Claude": {
        "nombre": "Deepseek (Alternativa)",
        "clave": CLAUDE_API_KEY,
        "url": "https://api.deepseek.com/v1/chat/completions",  # Ajustar URL a Deepseek
        "modelo": "deepseek-chat"  # Ajustar modelo a Deepseek
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
    """Obtiene la configuración de una API por su nombre"""
    return APIS_DISPONIBLES.get(nombre_api, None)