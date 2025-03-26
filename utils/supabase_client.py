# utils/supabase_client.py
from supabase import create_client
from typing import Optional

# Configuración de Supabase
SUPABASE_URL = "https://qjpcfuyzhrnqcjxnyxcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqcGNmdXl6aHJucWNqeG55eGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNzUzODQsImV4cCI6MjA1NDY1MTM4NH0.vASDpURRLt5wf9ngGkCNkiT0c-XbillDLTW9KFqk9Tg"

# Variable para guardar la instancia del cliente
_supabase_client = None

def get_supabase_client():
    """
    Devuelve una instancia del cliente Supabase, creándola si no existe
    Utiliza el patrón Singleton para evitar crear múltiples conexiones
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Cliente Supabase inicializado correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar cliente Supabase: {e}")
            # Devolver None en caso de error
            return None
    
    return _supabase_client

# Funciones auxiliares para operaciones comunes

def fetch_by_id(table_name: str, id_value: int):
    """Obtiene un registro por su ID"""
    supabase = get_supabase_client()
    if not supabase:
        return None
        
    try:
        response = supabase.table(table_name).select("*").eq("id", id_value).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error al obtener registro por ID: {e}")
        return None

def fetch_all(table_name: str, limit: Optional[int] = 100):
    """Obtiene todos los registros de una tabla (con límite)"""
    supabase = get_supabase_client()
    if not supabase:
        return []
        
    try:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error al obtener todos los registros: {e}")
        return []

def insert_record(table_name: str, data: dict):
    """Inserta un nuevo registro"""
    supabase = get_supabase_client()
    if not supabase:
        return None
        
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error al insertar registro: {e}")
        return None

def update_record(table_name: str, id_value: int, data: dict):
    """Actualiza un registro existente"""
    supabase = get_supabase_client()
    if not supabase:
        return None
        
    try:
        response = supabase.table(table_name).update(data).eq("id", id_value).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error al actualizar registro: {e}")
        return None

def delete_record(table_name: str, id_value: int):
    """Elimina un registro"""
    supabase = get_supabase_client()
    if not supabase:
        return False
        
    try:
        response = supabase.table(table_name).delete().eq("id", id_value).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Error al eliminar registro: {e}")
        return False