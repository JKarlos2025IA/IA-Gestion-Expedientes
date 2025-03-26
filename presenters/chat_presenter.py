# presenters/chat_presenter.py
from typing import Dict, List, Any, Optional
import streamlit as st
import re
import datetime

class ChatPresenter:
    """
    Clase encargada de preparar los datos del chat para su visualización en Streamlit
    """
    
    def __init__(self):
        self.message_styles = {
            "user": {
                "background": "#2b313e",
                "border": "1px solid #4d5b7c",
                "border_radius": "10px 10px 0 10px"
            },
            "assistant": {
                "background": "#0e4261",
                "border": "1px solid #0e6efd",
                "border_radius": "10px 10px 10px 0"
            }
        }
    
    def format_message(self, message: Dict[str, Any]) -> str:
        """
        Formatea un mensaje para su visualización con markdown mejorado
        """
        content = message.get("content", "")
        
        # Reemplazar enlaces con formato markdown
        content = re.sub(r'(https?://\S+)', r'[\1](\1)', content)
        
        # Mejorar formato de listas
        content = re.sub(r'^\*\s', '• ', content, flags=re.MULTILINE)
        
        # Resaltar entidades importantes (números de expediente, etc.)
        content = self._highlight_entities(content)
        
        return content
    
    def _highlight_entities(self, text: str) -> str:
        """
        Resalta entidades importantes en el texto
        """
        # Resaltar números de expediente
        text = re.sub(r'(\d{4}-[A-Za-z]{3}-[A-Za-z]{3}-\d{4})', r'**\1**', text)
        
        # Resaltar fechas
        text = re.sub(r'(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})', r'*\1*', text)
        
        return text
    
    def display_message(self, message: Dict[str, Any]) -> None:
        """
        Muestra un mensaje formateado en Streamlit
        """
        role = message.get("role", "user")
        content = self.format_message(message)
        
        # Obtener estilo según el rol
        style = self.message_styles.get(role, self.message_styles["user"])
        
        # Crear el HTML para el mensaje con estilos personalizados
        html = f"""
        <div style="padding: 10px; 
                   background: {style['background']}; 
                   border: {style['border']}; 
                   border-radius: {style['border_radius']}; 
                   margin-bottom: 10px; 
                   max-width: 90%;">
            <p><strong>{"Tú" if role == "user" else "Asistente"}:</strong></p>
            <div>{content}</div>
        </div>
        """
        
        # Alinear mensajes: usuario a la derecha, asistente a la izquierda
        container = st.container()
        with container:
            if role == "user":
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.markdown(html, unsafe_allow_html=True)
    
    def display_conversation(self, messages: List[Dict[str, Any]]) -> None:
        """
        Muestra una conversación completa
        """
        for message in messages:
            self.display_message(message)
    
    def format_timestamp(self, timestamp: str) -> str:
        """
        Formatea una marca de tiempo para mostrarla de forma amigable
        """
        try:
            # Convertir el timestamp a datetime
            dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            # Obtener la fecha y hora actuales
            now = datetime.datetime.now(datetime.timezone.utc)
            
            # Calcular la diferencia
            diff = now - dt
            
            # Formatear la salida según la antigüedad
            if diff.days == 0:
                if diff.seconds < 60:
                    return "Hace unos segundos"
                elif diff.seconds < 3600:
                    return f"Hace {diff.seconds // 60} minutos"
                else:
                    return f"Hace {diff.seconds // 3600} horas"
            elif diff.days == 1:
                return "Ayer"
            elif diff.days < 7:
                return f"Hace {diff.days} días"
            elif diff.days < 30:
                return f"Hace {diff.days // 7} semanas"
            else:
                return dt.strftime("%d/%m/%Y")
        except:
            return timestamp
    
    def format_conversation_summary(self, conversation: Dict[str, Any], messages: List[Dict[str, Any]], max_preview: int = 2) -> Dict[str, Any]:
        """
        Crea un resumen de una conversación para mostrar en la lista
        """
        # Título de la conversación
        title = conversation.get("title", "Conversación sin título")
        
        # Fecha formateada
        created_at = self.format_timestamp(conversation.get("created_at", ""))
        
        # Resumen de los primeros mensajes
        preview = []
        for msg in messages[:max_preview]:
            role = "Tú" if msg.get("role") == "user" else "Asistente"
            content = msg.get("content", "")
            if len(content) > 60:
                content = content[:60] + "..."
            preview.append(f"{role}: {content}")
        
        # Conteo total de mensajes
        total_messages = len(messages)
        
        return {
            "id": conversation.get("id"),
            "title": title,
            "created_at": created_at,
            "preview": preview,
            "total_messages": total_messages
        }