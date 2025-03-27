# controllers/chat_controller.py
from typing import Dict, List, Any, Optional, Tuple
import re
import traceback
import uuid

from controllers.ia_controller import IAController
from controllers.busqueda_controller import BusquedaController
from models.chat_history_model import ChatHistoryModel

class ChatController:
    def __init__(self, api_name: str = "Claude", user_id: Optional[str] = "anonymous"):
        self.ia_controller = IAController(api_name)
        self.busqueda_controller = BusquedaController()
        self.chat_history = ChatHistoryModel()
        self.user_id = user_id
        self.current_conversation_id = None
        
        # Configuraciones para el historial y contexto
        self.max_context_messages = 10  # Máximo número de mensajes para el contexto
        self.include_system_prompt = True  # Si se debe incluir un prompt del sistema
        print(f"ChatController inicializado con API {api_name} y usuario {user_id}")
    
    def set_api(self, api_name: str) -> bool:
        """Cambia la API a utilizar"""
        return self.ia_controller.set_api(api_name)
    
    def set_user(self, user_id: str) -> None:
        """Establece el ID del usuario actual"""
        self.user_id = user_id
    
    def extract_keywords(self, query: str, min_length: int = 3) -> List[str]:
        """Extrae palabras clave de la consulta"""
        # Eliminar caracteres especiales y dividir en palabras
        words = re.findall(r'\b\w+\b', query.lower())
        
        # Filtrar palabras demasiado cortas y palabras vacías
        stopwords = {"de", "la", "el", "en", "y", "a", "los", "las", "un", "una", "unos", 
                     "unas", "al", "del", "lo", "para", "por", "con", "son", "como", "que",
                     "se", "su", "sus", "este", "esta", "estos", "estas"}
        
        keywords = [word for word in words if len(word) >= min_length and word not in stopwords]
        print(f"Palabras clave extraídas: {keywords}")
        return keywords
    
    def extract_expediente_numbers(self, query: str) -> List[str]:
        """Extrae números de expediente del formato estándar"""
        patron_expediente = r"\d{4}-[A-Za-z]{3}-[A-Za-z]{3}-\d{4}"
        expedientes = re.findall(patron_expediente, query)
        print(f"Números de expediente encontrados: {expedientes}")
        return expedientes
    
    def detect_query_intent(self, query: str) -> str:
        """
        Detecta la intención de la consulta para ajustar el formato de respuesta
        :param query: Texto de la consulta
        :return: 'simple', 'search', o 'report'
        """
        # Palabras indicadoras de intención
        simple_indicators = ["existe", "hay", "encuentra", "ubicar", "buscar", "hallar", "contiene"]
        search_indicators = ["busca", "encuentra", "dame", "muestra", "lista", "relacionados", "similares"]
        report_indicators = ["analiza", "informe", "reporte", "análisis", "resumen", "detalla", "explica", "evalúa"]
        
        query_lower = query.lower()
        
        # Verificar si es una consulta sobre existencia de expediente específico
        expediente_numbers = self.extract_expediente_numbers(query)
        if expediente_numbers and any(indicator in query_lower for indicator in simple_indicators):
            return "simple"
        
        # Verificar por palabras indicadoras de búsqueda
        if any(indicator in query_lower for indicator in search_indicators):
            return "search"
        
        # Verificar por palabras indicadoras de informe
        if any(indicator in query_lower for indicator in report_indicators):
            return "report"
        
        # Por defecto, asumimos que es una búsqueda general
        return "search"
    
    def create_conversation(self, title: Optional[str] = None, project_id: Optional[str] = None) -> Optional[str]:
        """Crea una nueva conversación y devuelve su ID"""
        try:
            if not title:
                title = "Nueva conversación"
                
            result = self.chat_history.create_conversation(self.user_id, project_id, title)
            if result:
                conversation_id = result.get("id")
                if conversation_id:
                    self.current_conversation_id = conversation_id
                    print(f"Conversación creada con ID: {conversation_id}")
                    return conversation_id
            
            print("Error: No se pudo crear conversación - resultado vacío")
            return None
        except Exception as e:
            print(f"Error al crear conversación: {str(e)}")
            print(traceback.format_exc())
            return None
    
    def set_conversation(self, conversation_id: str) -> bool:
        """Establece la conversación actual"""
        try:
            conversation = self.chat_history.get_conversation(conversation_id)
            if conversation:
                self.current_conversation_id = conversation_id
                return True
            return False
        except Exception as e:
            print(f"Error al establecer conversación: {str(e)}")
            return False
    
    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene el historial completo de una conversación"""
        try:
            conv_id = conversation_id or self.current_conversation_id
            if not conv_id:
                return []
                
            return self.chat_history.get_conversation_messages(conv_id)
        except Exception as e:
            print(f"Error al obtener historial de conversación: {str(e)}")
            return []
    
    def process_query(self, query: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario y devuelve la respuesta con metadatos
        :param query: Texto de la consulta
        :param conversation_id: ID de la conversación (opcional)
        :return: Diccionario con la respuesta y metadatos
        """
        try:
            # 1. Establecer la conversación o crear una nueva si es necesario
            conv_id = conversation_id or self.current_conversation_id
            if not conv_id:
                conv_id = self.create_conversation(f"Consulta: {query[:50]}...")
                if not conv_id:
                    return {"error": "No se pudo crear una conversación"}
            
            # 2. Guardar la consulta del usuario en el historial
            message_id = None
            user_message = self.chat_history.add_message(conv_id, "user", query)
            if user_message:
                message_id = user_message.get("id")
            
            # 3. Detectar la intención de la consulta
            intent = self.detect_query_intent(query)
            
            # 4. Extraer palabras clave y buscar información relevante
            keywords = self.extract_keywords(query)
            expediente_numbers = self.extract_expediente_numbers(query)
            
            print(f"Buscando información con {len(keywords)} palabras clave y {len(expediente_numbers)} números de expediente")
            relevant_info = self.busqueda_controller.search(keywords, expediente_numbers)
            
            # 5. Obtener los mensajes recientes para el contexto
            context_messages = self.chat_history.get_message_history_for_context(conv_id, self.max_context_messages)
            
            # 6. Preparar el mensaje del sistema con el contexto adaptado a la intención
            system_prompt = self._create_system_prompt(relevant_info, intent)
            
            # 7. Llamar a la API de IA con el contexto y la consulta
            print(f"Llamando a la API de IA con {len(context_messages)} mensajes de contexto")
            ia_response = self.ia_controller.call_api(context_messages, system_prompt)
            
            # 8. Guardar la respuesta en el historial
            assistant_message = None
            if ia_response:
                assistant_message = self.chat_history.add_message(conv_id, "assistant", ia_response, {
                    "info_found": bool(relevant_info),
                    "keywords": keywords,
                    "expedientes": expediente_numbers,
                    "intent": intent
                })
            
            # 9. Devolver la respuesta con metadatos
            return {
                "response": ia_response,
                "conversation_id": conv_id,
                "info_found": bool(relevant_info),
                "intent": intent,
                "message_id": assistant_message.get("id") if assistant_message else None
            }
        except Exception as e:
            print(f"Error al procesar consulta: {str(e)}")
            print(traceback.format_exc())
            return {"error": f"Error al procesar la consulta: {str(e)}"}
    
    def _create_system_prompt(self, relevant_info: Dict[str, Any], intent: str = "search") -> str:
        """
        Crea un prompt del sistema con la información relevante encontrada
        adaptado a la intención detectada en la consulta
        :param relevant_info: Información relevante encontrada
        :param intent: Intención detectada ('simple', 'search' o 'report')
        :return: Prompt del sistema
        """
        # Base común para todos los tipos de intención
        base_prompt = """Eres un asistente jurídico especializado en gestión de expedientes."""
        
        # Diferentes instrucciones según la intención
        if intent == "simple":
            # Para consultas simples (existencia de expedientes, preguntas directas)
            prompt = f"""{base_prompt}
            
Responde de manera breve y directa a la consulta. Si la pregunta es sobre la existencia de un expediente específico, 
simplemente indica si existe o no y proporciona los datos básicos sin elaborar demasiado.

Instrucciones:
1. Sé conciso. Responde directamente a lo que se pregunta.
2. Evita largas explicaciones o desarrollo de ideas.
3. Utiliza frases cortas y directo al punto.
4. No elabores análisis o interpretaciones a menos que se soliciten explícitamente.
"""
        elif intent == "search":
            # Para búsquedas generales
            prompt = f"""{base_prompt}
            
Responde de manera informativa a la consulta, enfocándote en proporcionar los datos solicitados
de forma organizada y clara.

Instrucciones:
1. Presenta los resultados de manera estructurada y fácil de leer.
2. Organiza la información en listas o puntos cuando sea apropiado.
3. Destaca los datos clave relevantes a la consulta.
4. Mantén un equilibrio entre ser conciso y proporcionar suficiente contexto.
"""
        else:  # intent == "report"
            # Para solicitudes de informes detallados
            prompt = f"""{base_prompt}
            
Responde de manera profesional y detallada, generando un informe completo sobre el tema consultado.

Instrucciones:
1. Estructura tu respuesta con introducción, desarrollo y conclusión.
2. Proporciona análisis detallado de la información disponible.
3. Incluye recomendaciones o interpretaciones cuando sea apropiado.
4. Utiliza un tono formal y profesional propio de un informe jurídico.
5. Contextualiza la información dentro del marco normativo relevante.
"""

        # Añadir información de expedientes si se encontró
        has_info = False
        
        if "expedientes" in relevant_info and relevant_info["expedientes"]:
            has_info = True
            prompt += "\n\n## Expedientes encontrados:\n"
            for i, exp in enumerate(relevant_info["expedientes"][:5], 1):
                prompt += f"\n### Expediente {i}:\n"
                for field, value in exp.items():
                    if field not in ["id", "created_at", "updated_at"] and value:
                        prompt += f"- {field}: {value}\n"
        
        # Añadir información de documentos si se encontró
        if "documentos" in relevant_info and relevant_info["documentos"]:
            has_info = True
            prompt += "\n\n## Documentos relevantes:\n"
            for i, doc in enumerate(relevant_info["documentos"][:7], 1):
                prompt += f"\n### Documento {i}:\n"
                # Mostrar tipo y nombre del documento
                if "tipo_documento" in doc:
                    prompt += f"- Tipo: {doc['tipo_documento']}\n"
                if "nombre_archivo" in doc:
                    prompt += f"- Archivo: {doc['nombre_archivo']}\n"
                
                # Mostrar extracto del contenido
                if "contenido" in doc and doc["contenido"]:
                    contenido = doc["contenido"]
                    if len(contenido) > 300:
                        contenido = contenido[:300] + "..."
                    prompt += f"- Extracto: {contenido}\n"
                
                # Mostrar información del expediente relacionado
                if "expediente_numero" in doc:
                    prompt += f"- Pertenece al expediente: {doc['expediente_numero']}\n"
        
        # Añadir información de normativas si se encontró
        if "normativas" in relevant_info and relevant_info["normativas"]:
            has_info = True
            prompt += "\n\n## Normativas relacionadas:\n"
            for i, norm in enumerate(relevant_info["normativas"][:3], 1):
                tabla = norm.get("tabla", "").replace("normativa_", "").capitalize()
                palabra = norm.get("palabra_clave", "")
                prompt += f"\n### {tabla} relacionados con '{palabra}':\n"
                
                for j, item in enumerate(norm.get("datos", [])[:2], 1):
                    prompt += f"- Registro {j}:\n"
                    for key, value in item.items():
                        if key not in ["id", "created_at", "updated_at"] and value is not None:
                            # Limitar tamaño de valores largos
                            str_value = str(value)
                            if len(str_value) > 100:
                                str_value = str_value[:100] + "..."
                            prompt += f"  * {key}: {str_value}\n"
        
        # Si no se encontró información, indicarlo
        if not has_info:
            prompt += "\n\nNo se encontró información específica en la base de datos sobre esta consulta."
            # Para consultas simples, indicar claramente si no se encuentra un expediente
            if intent == "simple" and len(self.extract_expediente_numbers(query)) > 0:
                prompt += " Los expedientes mencionados en la consulta no existen en el sistema."
        
        return prompt
    
    def update_message(self, message_id: str, content: str) -> bool:
        """Actualiza el contenido de un mensaje"""
        try:
            return self.chat_history.update_message(message_id, content)
        except Exception as e:
            print(f"Error al actualizar mensaje: {str(e)}")
            return False
    
    def delete_message(self, message_id: str) -> bool:
        """Elimina un mensaje específico"""
        try:
            return self.chat_history.delete_message(message_id)
        except Exception as e:
            print(f"Error al eliminar mensaje: {str(e)}")
            return False
    
    def rename_conversation(self, conversation_id: str, title: str) -> bool:
        """Cambia el título de una conversación"""
        try:
            return self.chat_history.update_conversation_title(conversation_id, title)
        except Exception as e:
            print(f"Error al renombrar conversación: {str(e)}")
            return False
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Elimina una conversación y todos sus mensajes"""
        try:
            success = self.chat_history.delete_conversation(conversation_id)
            if success and self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
            return success
        except Exception as e:
            print(f"Error al eliminar conversación: {str(e)}")
            return False
    
    def get_user_conversations(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene todas las conversaciones del usuario actual"""
        try:
            return self.chat_history.get_user_conversations(self.user_id, project_id)
        except Exception as e:
            print(f"Error al obtener conversaciones del usuario: {str(e)}")
            return []