import requests
import json
import time
import os

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

def crear_tabla_si_no_existe(nombre_tabla, definicion_sql):
    """
    Crea una tabla en Supabase si no existe
    :param nombre_tabla: Nombre de la tabla a crear
    :param definicion_sql: SQL para crear la tabla
    :return: True si la operación fue exitosa
    """
    # URL para el endpoint RPC de Supabase
    url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
    
    # Datos para la solicitud
    data = {
        "query": definicion_sql
    }
    
    print(f"Intentando crear tabla: {nombre_tabla}")
    
    try:
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, json=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code in [200, 201]:
            print(f"✅ Tabla '{nombre_tabla}' creada o ya existente.")
            return True
        else:
            print(f"❌ Error al crear tabla '{nombre_tabla}': {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción al crear tabla '{nombre_tabla}': {str(e)}")
        return False

def verificar_tabla_existe(nombre_tabla):
    """
    Verifica si una tabla existe en Supabase
    :param nombre_tabla: Nombre de la tabla a verificar
    :return: True si la tabla existe
    """
    # URL para consultar esquema de información
    url = f"{SUPABASE_URL}/rest/v1/information_schema/tables?select=table_name&table_name=eq.{nombre_tabla}"
    
    try:
        # Realizar la solicitud GET
        response = requests.get(url, headers=headers)
        
        # Verificar si la tabla existe
        return len(response.json()) > 0
    except Exception as e:
        print(f"❌ Error al verificar tabla '{nombre_tabla}': {str(e)}")
        return False

def main():
    print("🚀 Iniciando configuración de tablas en Supabase...")
    
    # SQL para crear la tabla de conversaciones
    sql_conversaciones = """
    CREATE TABLE IF NOT EXISTS chat_conversations (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id TEXT NOT NULL,
        project_id TEXT,
        title TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    # SQL para crear la tabla de mensajes
    sql_mensajes = """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        conversation_id UUID REFERENCES chat_conversations(id) ON DELETE CASCADE,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata JSONB,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    # SQL para crear la tabla de proyectos
    sql_proyectos = """
    CREATE TABLE IF NOT EXISTS projects (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    # Crear tablas
    if not verificar_tabla_existe("chat_conversations"):
        crear_tabla_si_no_existe("chat_conversations", sql_conversaciones)
        time.sleep(1)  # Esperar un segundo entre creaciones para evitar límites de API
    else:
        print("✅ Tabla 'chat_conversations' ya existe.")
    
    if not verificar_tabla_existe("chat_messages"):
        crear_tabla_si_no_existe("chat_messages", sql_mensajes)
        time.sleep(1)
    else:
        print("✅ Tabla 'chat_messages' ya existe.")
    
    if not verificar_tabla_existe("projects"):
        crear_tabla_si_no_existe("projects", sql_proyectos)
    else:
        print("✅ Tabla 'projects' ya existe.")
    
    print("✨ Configuración de tablas completada.")
    
    # Verificación final
    tablas = ["chat_conversations", "chat_messages", "projects"]
    todas_existen = True
    
    for tabla in tablas:
        if verificar_tabla_existe(tabla):
            print(f"✅ Verificado: Tabla '{tabla}' existe.")
        else:
            print(f"❌ Verificado: Tabla '{tabla}' NO existe.")
            todas_existen = False
    
    if todas_existen:
        print("🎉 Todas las tablas fueron creadas correctamente.")
    else:
        print("⚠️ Algunas tablas no pudieron ser creadas. Revisa los errores anteriores.")

if __name__ == "__main__":
    main()