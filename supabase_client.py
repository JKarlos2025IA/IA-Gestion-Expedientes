# -*- coding: utf-8 -*-
import os
from supabase import create_client

# ConfiguraciÃ³n de Supabase
SUPABASE_URL = "https://qjpcfuyzhrnqcjxnyxcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqcGNmdXl6aHJucWNqeG55eGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNzUzODQsImV4cCI6MjA1NDY1MTM4NH0.vASDpURRLt5wf9ngGkCNkiT0c-XbillDLTW9KFqk9Tg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función para buscar un expediente con documentos relacionados
def buscar_expediente_completo(numero_expediente):
    try:
        # Buscar el expediente
        expediente_res = (
            supabase.table("expedientes")
            .select("*")
            .eq("numero_expediente", numero_expediente)
            .execute()
        )

        # Buscar los documentos relacionados al expediente
        documentos_res = (
            supabase.table("documentos_expediente")
            .select("*")
            .eq("expediente_id", expediente_res.data[0]["id"])
            .execute()
        ) if expediente_res.data else None

        # Si se encontró el expediente, devolver la información
        if expediente_res.data:
            return {
                "expediente": expediente_res.data[0],
                "documentos": documentos_res.data if documentos_res else "No hay documentos"
            }
        else:
            return None

    except Exception as e:
        print(f"Error al buscar expediente: {e}")
        return None