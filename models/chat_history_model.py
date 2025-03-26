# models/chat_history_model.py
from utils.supabase_client import get_supabase_client
from typing import Dict, List, Optional, Any
import datetime

class ChatHistoryModel:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.conversations_table = "chat_conversations"
        self.messages_table = "chat_messages"
        
        # Verificar si las tablas existen, y crearlas si no
        self._ensure_tables_exist()
    
    def _ensure_tables_exist(self):
        """Asegura que las tablas necesarias existen en Supabase"""
        try:
            # Verificar si las tablas existen consultando sus datos
            self.supabase.table(self.conversations_table).select("count").limit(1).execute()
            self.supabase.table(self.messages_table).select("count").limit(1).execute()
            print("✅ Tablas de chat verificadas")
        except Exception as e:
            print(f"⚠️ Error al verificar tablas: {e}")
            print("⏳ Intentando crear tablas de chat...")
            # Aquí podrías implementar la creación de tablas si lo necesitas
            # Nota: Esto requeriría permisos especiales en Supabase
    
    def create_conversation(self, user_id: str, project_id: Optional[str] = None, title: str = "Nueva conversación") -> Optional[Dict[str, Any]]:
        """Crea una nueva conversación"""
        try:
            data = {
                "user_id": user_id,
                "title": title,
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat()
            }
            
            if project_id:
                data["project_id"] = project_id
                
            response = self.supabase.table(self.conversations_table).insert(data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al crear conversación: {e}")
            return None
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una conversación por su ID"""
        try:
            response = (
                self.supabase.table(self.conversations_table)
                .select("*")
                .eq("id", conversation_id)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al obtener conversación: {e}")
            return None
    
    def get_user_conversations(self, user_id: str, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene todas las conversaciones de un usuario, opcionalmente filtradas por proyecto"""
        try:
            query = self.supabase.table(self.conversations_table).select("*").eq("user_id", user_id)
            
            if project_id:
                query = query.eq("project_id", project_id)
                
            response = query.order("updated_at", desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al obtener conversaciones del usuario: {e}")
            return []
    
    def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """Actualiza el título de una conversación"""
        try:
            data = {
                "title": title,
                "updated_at": datetime.datetime.now().isoformat()
            }
            
            response = (
                self.supabase.table(self.conversations_table)
                .update(data)
                .eq("id", conversation_id)
                .execute()
            )
            
            return bool(response.data)
        except Exception as e:
            print(f"Error al actualizar título de conversación: {e}")
            return False
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Elimina una conversación y todos sus mensajes"""
        try:
            # Primero eliminar todos los mensajes asociados
            self.supabase.table(self.messages_table).delete().eq("conversation_id", conversation_id).execute()
            
            # Luego eliminar la conversación
            response = (
                self.supabase.table(self.conversations_table)
                .delete()
                .eq("id", conversation_id)
                .execute()
            )
            
            return bool(response.data)
        except Exception as e:
            print(f"Error al eliminar conversación: {e}")
            return False
    
    def add_message(self, conversation_id: str, role: str, content: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Añade un nuevo mensaje a una conversación"""
        try:
            data = {
                "conversation_id": conversation_id,
                "role": role,  # "user" o "assistant"
                "content": content,
                "created_at": datetime.datetime.now().isoformat()
            }
            
            if metadata:
                data["metadata"] = metadata
                
            # Actualizar timestamp de la conversación
            self.supabase.table(self.conversations_table).update({
                "updated_at": datetime.datetime.now().isoformat()
            }).eq("id", conversation_id).execute()
                
            response = self.supabase.table(self.messages_table).insert(data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al añadir mensaje: {e}")
            return None
    
    def get_conversation_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los mensajes de una conversación ordenados cronológicamente"""
        try:
            response = (
                self.supabase.table(self.messages_table)
                .select("*")
                .eq("conversation_id", conversation_id)
                .order("created_at")
                .execute()
            )
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al obtener mensajes de la conversación: {e}")
            return []
    
    def delete_message(self, message_id: str) -> bool:
        """Elimina un mensaje específico"""
        try:
            response = (
                self.supabase.table(self.messages_table)
                .delete()
                .eq("id", message_id)
                .execute()
            )
            
            return bool(response.data)
        except Exception as e:
            print(f"Error al eliminar mensaje: {e}")
            return False
    
    def update_message(self, message_id: str, content: str) -> bool:
        """Actualiza el contenido de un mensaje"""
        try:
            response = (
                self.supabase.table(self.messages_table)
                .update({"content": content})
                .eq("id", message_id)
                .execute()
            )
            
            return bool(response.data)
        except Exception as e:
            print(f"Error al actualizar mensaje: {e}")
            return False
    
    def get_message_history_for_context(self, conversation_id: str, max_messages: int = 10) -> List[Dict[str, str]]:
        """
        Obtiene los mensajes recientes para usar como contexto en nuevas consultas a la IA
        Devuelve una lista de diccionarios {role, content} en formato adecuado para APIs
        """
        try:
            response = (
                self.supabase.table(self.messages_table)
                .select("role,content")
                .eq("conversation_id", conversation_id)
                .order("created_at", desc=True)
                .limit(max_messages)
                .execute()
            )
            
            # Invertir para que estén en orden cronológico
            messages = response.data if response.data else []
            messages.reverse()
            
            return messages
        except Exception as e:
            print(f"Error al obtener historial para contexto: {e}")
            return []