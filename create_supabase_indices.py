import requests
import time

# Configuración de Supabase - Asegúrate de usar tus credenciales reales
SUPABASE_URL = "https://qjpcfuyzhrnqcjxnyxcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqcGNmdXl6aHJucWNqeG55eGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNzUzODQsImV4cCI6MjA1NDY1MTM4NH0.vASDpURRLt5wf9ngGkCNkiT0c-XbillDLTW9KFqk9Tg"

# Headers necesarios para las solicitudes
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def ejecutar_sql(query):
    """
    Ejecuta una consulta SQL personalizada en Supabase
    :param query: Consulta SQL a ejecutar
    :return: True si la operación fue exitosa
    """
    # URL para el endpoint RPC de Supabase
    url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
    
    # Datos para la solicitud
    data = {
        "query": query
    }
    
    try:
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, json=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code in [200, 201]:
            print(f"✅ SQL ejecutado correctamente.")
            return True
        else:
            print(f"❌ Error al ejecutar SQL: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción al ejecutar SQL: {str(e)}")
        return False

def main():
    print("🚀 Creando índices para optimizar consultas...")
    
    # Lista de índices a crear
    indices = [
        # Índices para tabla de conversaciones
        "CREATE INDEX IF NOT EXISTS idx_chat_conversations_user_id ON chat_conversations (user_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_conversations_project_id ON chat_conversations (project_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_conversations_updated_at ON chat_conversations (updated_at DESC);",
        
        # Índices para tabla de mensajes
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_id ON chat_messages (conversation_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_role ON chat_messages (role);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages (created_at);",
        
        # Índices para tabla de proyectos
        "CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects (user_id);",
        "CREATE INDEX IF NOT EXISTS idx_projects_name ON projects (name);",
        
        # Índices para búsqueda full-text (si está habilitado en tu plan de Supabase)
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_content_tsvector ON chat_messages USING GIN (to_tsvector('spanish', content));"
    ]
    
    # Ejecutar creación de cada índice
    for i, indice_sql in enumerate(indices):
        print(f"Creando índice {i+1}/{len(indices)}...")
        ejecutar_sql(indice_sql)
        time.sleep(0.5)  # Pequeña pausa para no sobrecargar la API
    
    print("✨ Creación de índices completada.")

if __name__ == "__main__":
    main()