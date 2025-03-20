# -*- coding: utf-8 -*-
import os
import requests
import json
from config import CLAUDE_API_KEY
from supabase_client import buscar_informacion_para_chat

# Verificar si la API key está definida correctamente
if not CLAUDE_API_KEY or CLAUDE_API_KEY == "CLAVE_NO_ENCONTRADA":
    print("⚠️ ERROR: La clave de API de Claude no está configurada correctamente.")
else:
    print(f"✅ Claude API Key detectada: {CLAUDE_API_KEY[:5]}********")

# Función para formatear mejor los datos del expediente
def formatear_expediente(expediente):
    info = []
    
    # Campos principales
    campos_principales = [
        ("Número", "numero_expediente"),
        ("Fecha de creación", "fecha_creacion"),
        ("Tipo de proceso", "tipo_proceso"),
        ("Modalidad", "modalidad"),
        ("Sección", "seccion"),
        ("Tema principal", "tema_principal"),
        ("Área solicitante", "area_solicitante"),
        ("Estado", "estado")
    ]
    
    for label, campo in campos_principales:
        if campo in expediente and expediente[campo]:
            info.append(f"{label}: {expediente[campo]}")
    
    return info

# Función para formatear mejor los datos de documentos
def formatear_documento(documento):
    info = []
    
    # Campos principales para documentos
    if "tipo_documento" in documento and documento["tipo_documento"]:
        info.append(f"Tipo: {documento['tipo_documento']}")
    
    if "nombre_archivo" in documento and documento["nombre_archivo"]:
        info.append(f"Archivo: {documento['nombre_archivo']}")
    
    if "contenido" in documento and documento["contenido"]:
        # Limitar el tamaño del contenido
        contenido = documento["contenido"]
        if len(contenido) > 300:
            contenido = contenido[:300] + "..."
        info.append(f"Extracto: {contenido}")
    
    # Información del expediente relacionado
    if "expediente_numero" in documento and documento["expediente_numero"]:
        info.append(f"Pertenece al expediente: {documento['expediente_numero']}")
    
    return info

# Función para hacer la llamada a la API de Claude con contexto de la base de datos
def consulta_claude(mensaje):
    url = "https://api.anthropic.com/v1/messages"  # URL de la API
    headers = {
        "anthropic-version": "2023-06-01",
        "x-api-key": CLAUDE_API_KEY,
        "content-type": "application/json"
    }

    # Paso 1: Buscar información relevante en Supabase
    print("Buscando información relevante en la base de datos...")
    informacion_bd = buscar_informacion_para_chat(mensaje)
    
    # Paso 2: Preparar el contexto con la información encontrada
    contexto = ""
    
    # Si encontramos expedientes relevantes
    if informacion_bd and "expedientes" in informacion_bd and informacion_bd["expedientes"]:
        contexto += "\n\n## Expedientes encontrados:\n"
        for i, exp in enumerate(informacion_bd["expedientes"][:5], 1):  # Limitamos a 5
            contexto += f"\n### Expediente {i}:\n"
            for linea in formatear_expediente(exp):
                contexto += f"- {linea}\n"
    
    # Si encontramos documentos relevantes
    if informacion_bd and "documentos" in informacion_bd and informacion_bd["documentos"]:
        contexto += "\n\n## Documentos relevantes:\n"
        for i, doc in enumerate(informacion_bd["documentos"][:7], 1):  # Limitamos a 7
            contexto += f"\n### Documento {i}:\n"
            for linea in formatear_documento(doc):
                contexto += f"- {linea}\n"
    
    # Si encontramos normativas relevantes
    if informacion_bd and "normativas" in informacion_bd and informacion_bd["normativas"]:
        contexto += "\n\n## Normativas relacionadas:\n"
        for i, norm in enumerate(informacion_bd["normativas"][:3], 1):  # Limitamos a 3
            tabla = norm.get("tabla", "").replace("normativa_", "").capitalize()
            palabra = norm.get("palabra_clave", "")
            contexto += f"\n### {tabla} relacionados con '{palabra}':\n"
            
            for j, item in enumerate(norm.get("datos", [])[:2], 1):  # Limitamos a 2 items por normativa
                contexto += f"- Registro {j}:\n"
                # Mostrar campos relevantes
                for key, value in item.items():
                    if key not in ["id", "created_at", "updated_at"] and value is not None:
                        # Limitar el tamaño de los valores
                        str_value = str(value)
                        if len(str_value) > 100:
                            str_value = str_value[:100] + "..."
                        contexto += f"  * {key}: {str_value}\n"
    
    # Si no encontramos información, indicarlo
    if not contexto:
        contexto = "\nNo se encontró información específica en la base de datos sobre esta consulta."
    
    print(f"Contexto generado: {len(contexto)} caracteres")
    
    # Paso 3: Crear mensaje para Claude con el contexto
    mensaje_con_contexto = f"""Eres un asistente jurídico especializado en gestión de expedientes. Responde de manera profesional y detallada a la siguiente consulta utilizando la información de la base de datos proporcionada.

Consulta del usuario: {mensaje}

Información disponible en la base de datos:
{contexto}

Instrucciones:
1. Responde directamente a la consulta del usuario basándote en la información proporcionada.
2. Si la información es insuficiente, indica qué datos adicionales serían necesarios.
3. Organiza tu respuesta de manera clara y estructurada, con introducción, desarrollo y conclusión.
4. Cuando sea apropiado, incluye sugerencias o recomendaciones sobre los próximos pasos a seguir.
5. Utiliza un tono profesional pero accesible, como lo haría un asesor jurídico experimentado.
"""

    data = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": mensaje_con_contexto}]
    }

    try:
        print("Enviando consulta a Claude...")
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Status code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text[:500]}")
        
        response_json = response.json()

        if response.status_code == 200:
            # Extraer el texto de la respuesta
            if "content" in response_json:
                # Encontrar el texto en la respuesta
                for item in response_json.get("content", []):
                    if item.get("type") == "text":
                        return item.get("text", "")
                return "⚠️ La respuesta no contiene texto."
            else:
                return "⚠️ La API no devolvió contenido en la respuesta."
        else:
            error_message = response_json.get("error", {}).get("message", "Error desconocido")
            return f"❌ Error en la consulta: {error_message}"

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
        return f"🚨 Error en la conexión con la API: {str(e)}"
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return f"🚨 Error inesperado: {str(e)}"