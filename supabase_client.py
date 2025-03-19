from supabase import create_client

# Configurar la conexión con Supabase
SUPABASE_URL = "https://qjpcfuyzhrnqcjxnyxcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqcGNmdXl6aHJucWNqeG55eGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNzUzODQsImV4cCI6MjA1NDY1MTM4NH0.vASDpURRLt5wf9ngGkCNkiT0c-XbillDLTW9KFqk9Tg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def buscar_expediente(numero_expediente):
    """Busca un expediente en la base de datos."""
    respuesta = supabase.table("expedientes").select("*").eq("numero_expediente", numero_expediente).execute()
    return respuesta.data if respuesta.data else None

def buscar_expediente_completo(numero_expediente):
    """Busca un expediente y sus documentos relacionados en la base de datos."""
    try:
        # Buscar expediente
        expediente_res = supabase.table("expedientes").select("*").eq("numero_expediente", numero_expediente).execute()

        if not expediente_res.data:
            return None  # No se encontró el expediente
        
        expediente_id = expediente_res.data[0]["id"]  # Extraer el ID del expediente
        
        # Buscar documentos relacionados
        documentos_res = supabase.table("documentos_expediente").select("*").eq("expediente_id", expediente_id).execute()

        return {
            "expediente": expediente_res.data[0],  # Tomar solo el primer expediente encontrado
            "documentos": documentos_res.data  # Lista de documentos asociados
        }
    except Exception as e:
        print(f"Error al buscar expediente: {e}")
        return None
