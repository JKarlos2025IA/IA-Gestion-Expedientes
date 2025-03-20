# -*- coding: utf-8 -*-
import os
from supabase import create_client

# Configuración de Supabase
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

        # Si no se encontró el expediente, retornar None
        if not expediente_res.data:
            return None
            
        # Obtener el ID del expediente
        expediente_id = expediente_res.data[0]["id"]
        
        # Buscar los documentos relacionados al expediente
        documentos_res = (
            supabase.table("documentos_expediente")
            .select("*")
            .eq("expediente_id", expediente_id)
            .execute()
        )

        # Retornar los resultados
        return {
            "expediente": expediente_res.data[0],
            "documentos": documentos_res.data if documentos_res.data else "No hay documentos"
        }

    except Exception as e:
        print(f"Error al buscar expediente: {e}")
        return None

# Nueva función: búsqueda avanzada para el chat con relaciones entre tablas
def buscar_informacion_para_chat(consulta):
    try:
        # Palabras clave de la consulta (simplificado - se puede mejorar)
        palabras_clave = [palabra.lower() for palabra in consulta.split() if len(palabra) > 3]
        print(f"Palabras clave extraídas: {palabras_clave}")
        
        resultados = {
            "expedientes": [],
            "documentos": [],
            "normativas": []
        }
        
        # Extraer números de expedientes mencionados en la consulta
        import re
        patron_expediente = r"\d{4}-[A-Za-z]{3}-[A-Za-z]{3}-\d{4}"
        expedientes_mencionados = re.findall(patron_expediente, consulta)
        
        # 1. Primero, buscar expedientes específicos por número
        if expedientes_mencionados:
            print(f"Expedientes mencionados en la consulta: {expedientes_mencionados}")
            for num_exp in expedientes_mencionados:
                try:
                    response = supabase.table("expedientes").select("*").ilike("numero_expediente", num_exp).execute()
                    if response.data:
                        print(f"Expediente encontrado por número: {num_exp}")
                        resultados["expedientes"].extend(response.data)
                except Exception as e:
                    print(f"Error al buscar expediente por número {num_exp}: {e}")
        
        # 2. Buscar en expedientes por palabras clave
        for campo in ["numero_expediente", "tipo_proceso", "tema_principal", "area_solicitante", "seccion"]:
            for palabra in palabras_clave:
                try:
                    response = supabase.table("expedientes").select("*").ilike(campo, f"%{palabra}%").execute()
                    if response.data:
                        print(f"Encontrados {len(response.data)} expedientes con '{palabra}' en '{campo}'")
                        resultados["expedientes"].extend(response.data)
                except Exception as e:
                    print(f"Error al buscar en expedientes.{campo}: {e}")
        
        # Eliminar duplicados de expedientes
        expedientes_unicos = {}
        for exp in resultados["expedientes"]:
            expedientes_unicos[exp["id"]] = exp
        resultados["expedientes"] = list(expedientes_unicos.values())
        
        # 3. Buscar documentos relacionados con los expedientes encontrados
        print("Buscando documentos relacionados con los expedientes encontrados...")
        for expediente in resultados["expedientes"]:
            try:
                exp_id = expediente["id"]
                docs_response = supabase.table("documentos_expediente").select("*").eq("expediente_id", exp_id).execute()
                
                if docs_response.data:
                    print(f"Encontrados {len(docs_response.data)} documentos para el expediente {expediente.get('numero_expediente', exp_id)}")
                    # Añadir información del expediente a cada documento
                    for doc in docs_response.data:
                        doc["expediente_numero"] = expediente.get("numero_expediente", "")
                        doc["expediente_tipo"] = expediente.get("tipo_proceso", "")
                    
                    resultados["documentos"].extend(docs_response.data)
            except Exception as e:
                print(f"Error al buscar documentos para el expediente {expediente.get('id')}: {e}")
        
        # 4. Buscar también directamente en documentos_expediente por palabras clave en contenido
        print("Buscando en el contenido de los documentos...")
        for palabra in palabras_clave:
            try:
                response = supabase.table("documentos_expediente").select("*").ilike("contenido", f"%{palabra}%").execute()
                if response.data:
                    print(f"Encontrados {len(response.data)} documentos con '{palabra}' en 'contenido'")
                    
                    # Para cada documento, obtener información del expediente relacionado
                    for doc in response.data:
                        try:
                            if "expediente_id" in doc:
                                exp_response = supabase.table("expedientes").select("*").eq("id", doc["expediente_id"]).execute()
                                if exp_response.data:
                                    doc["expediente_numero"] = exp_response.data[0].get("numero_expediente", "")
                                    doc["expediente_tipo"] = exp_response.data[0].get("tipo_proceso", "")
                        except Exception as e:
                            print(f"Error al obtener expediente para documento: {e}")
                    
                    resultados["documentos"].extend(response.data)
            except Exception as e:
                print(f"Error al buscar en documentos por contenido: {e}")
        
        # Eliminar duplicados de documentos
        documentos_unicos = {}
        for doc in resultados["documentos"]:
            if "id" in doc:
                documentos_unicos[doc["id"]] = doc
        resultados["documentos"] = list(documentos_unicos.values())
        
        # 5. Buscar en normativas (si es relevante)
        tablas_normativa = [
            "normativa_anexos", "normativa_articulos", "normativa_disposiciones", 
            "normativa_documentos", "normativa_estructura", "normativa_literales", 
            "normativa_numerales", "normativa_referencias"
        ]
        
        for tabla in tablas_normativa:
            try:
                # Consultar si la tabla existe
                muestra = supabase.table(tabla).select("*").limit(1).execute()
                
                if muestra.data:
                    # Obtener columnas de la tabla
                    columnas = list(muestra.data[0].keys())
                    columnas_texto = [col for col in columnas if col not in ["id", "created_at", "updated_at"]]
                    
                    for columna in columnas_texto:
                        for palabra in palabras_clave:
                            try:
                                response = supabase.table(tabla).select("*").ilike(columna, f"%{palabra}%").limit(5).execute()
                                if response.data:
                                    print(f"Encontrados {len(response.data)} registros en {tabla} con '{palabra}' en '{columna}'")
                                    resultados["normativas"].append({
                                        "tabla": tabla,
                                        "columna": columna,
                                        "palabra_clave": palabra,
                                        "datos": response.data
                                    })
                            except Exception as e:
                                # Error específico por columna - no interrumpir el proceso general
                                pass
            except Exception as e:
                print(f"Error al consultar tabla {tabla}: {e}")
        
        print(f"Resultados finales: {len(resultados['expedientes'])} expedientes, {len(resultados['documentos'])} documentos, {len(resultados['normativas'])} grupos de normativas")
        return resultados
    except Exception as e:
        print(f"Error general en búsqueda avanzada: {str(e)}")
        return {"error": str(e)}