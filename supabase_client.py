# -*- coding: utf-8 -*-
from supabase import create_client

# Configuración de Supabase
SUPABASE_URL = "https://qjpcfuyzhrnqcjxnyxcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqcGNmdXl6aHJucWNqeG55eGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNzUzODQsImV4cCI6MjA1NDY1MTM4NH0.vASDpURRLt5wf9ngGkCNkiT0c-XbillDLTW9KFqk9Tg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def buscar_en_toda_bd(consulta):
    """
    Busca una palabra clave o frase en todas las tablas relevantes de la base de datos.
    """
    try:
        # Buscar en la tabla de expedientes
        expedientes_res = supabase.table("expedientes").select("*").ilike("numero_expediente", f"%{consulta}%").execute()

        expediente_id = None  # Inicializar expediente_id

        if expedientes_res.data and len(expedientes_res.data) > 0:
            expediente_id = expedientes_res.data[0]["id"]  # Extraer el ID del primer expediente encontrado

        # Buscar en la tabla de documentos solo si hay un expediente relacionado
        if expediente_id:
            documentos_res = supabase.table("documentos_expediente").select("*").eq("expediente_id", expediente_id).execute()
            documentos = documentos_res.data if documentos_res.data else "No encontrado"
        else:
            documentos = "No encontrado"

        # Formatear la respuesta final
        resultados = {
            "expedientes": expedientes_res.data if expedientes_res.data else "No encontrado",
            "documentos": documentos,
        }

        print("📌 Resultado antes de devolver:", resultados)  # Para depuración
        return resultados

    except Exception as e:
        print(f"Error al buscar en la base de datos: {e}")
        return None
