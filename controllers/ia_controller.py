# controllers/ia_controller.py
import os
import requests
import json
import traceback
from typing import Dict, List, Any, Optional
from config import APIS_DISPONIBLES

class IAController:
    def __init__(self, api_name: str = "Claude"):
        # Variable para depuraciÃ³n - definir primero
        self.debug_mode = True
        # Ahora configurar la API
        self.set_api(api_name)
    
    def set_api(self, api_name: str) -> bool:
        """Configura la API a utilizar"""
        if api_name in APIS_DISPONIBLES:
            self.api_config = APIS_DISPONIBLES[api_name]
            self.api_name = api_name
            if self.debug_mode:
                print(f"API configurada: {api_name}")
                # Mostrar los primeros 5 caracteres de la clave para verificaciÃ³n
                api_key = self.api_config.get("clave", "")
                masked_key = api_key[:5] + "*" * (len(api_key) - 5) if api_key else "No disponible"
                print(f"API Key: {masked_key}")
            return True
        print(f"API {api_name} no encontrada en configuraciÃ³n")
        return False
    
    def get_available_apis(self) -> List[str]:
        """Devuelve la lista de APIs disponibles"""
        return list(APIS_DISPONIBLES.keys())
    
    def _prepare_claude_payload(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> Dict[str, Any]:
        """Prepara el payload para la API de Claude o Deepseek"""
        # Si estamos usando Deepseek, ajustar el formato
        if "deepseek" in self.api_config.get("modelo", "").lower():
            # Formato para Deepseek
            formatted_messages = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "assistant"
                formatted_messages.append({"role": role, "content": msg["content"]})
            
            return {
                "model": self.api_config["modelo"],
                "messages": formatted_messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
        else:
            # Formato original para Claude
            return {
                "model": self.api_config["modelo"],
                "max_tokens": max_tokens,
                "messages": messages
            }
    
    def _prepare_gemini_payload(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Prepara el payload para la API de Gemini"""
        # Convertir formato de mensajes Claude a formato Gemini
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        return {
            "contents": gemini_messages,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
                "topP": 0.95,
                "topK": 40
            }
        }
    
    def call_api(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        """
        Llama a la API configurada con los mensajes proporcionados
        :param messages: Lista de mensajes en formato [{role, content}, ...]
        :param system_prompt: InstrucciÃ³n del sistema para APIs que lo soporten
        :return: Texto de respuesta o mensaje de error
        """
        if self.debug_mode:
            print(f"Llamando a API: {self.api_name}")
            print(f"Mensajes: {len(messages)}")
            if system_prompt:
                print(f"System prompt: {system_prompt[:50]}...")
        
        if self.api_name == "Claude":
            return self._call_claude_api(messages, system_prompt)
        elif self.api_name == "Gemini":
            return self._call_gemini_api(messages)
        else:
            return "âš ï¸ API no implementada o no reconocida."
    
    def _call_claude_api(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        """Realiza la llamada a la API de Claude o Deepseek"""
        url = self.api_config["url"]
        api_key = self.api_config["clave"]
        is_deepseek = "deepseek" in self.api_config.get("modelo", "").lower()
        
        # Headers diferentes segÃºn el proveedor
        if is_deepseek:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        else:
            headers = {
                "anthropic-version": "2023-06-01",
                "x-api-key": api_key,
                "content-type": "application/json"
            }
        
        # Si hay un system prompt, agregarlo como primer mensaje del sistema
        payload_messages = messages.copy()
        if system_prompt and not is_deepseek:
            payload_messages.insert(0, {"role": "system", "content": system_prompt})
        
        # Adecuar los mensajes para deepseek si es necesario
        if is_deepseek and system_prompt:
            # Para Deepseek, el system prompt debe ir como un mensaje del sistema al inicio
            payload_messages.insert(0, {"role": "system", "content": system_prompt})
        
        data = self._prepare_claude_payload(payload_messages)
        
        try:
            if self.debug_mode:
                print(f"Enviando consulta a {self.api_name} con {len(payload_messages)} mensajes...")
                print(f"URL: {url}")
                
                # Ocultar la clave API en la depuraciÃ³n
                debug_headers = {}
                for k, v in headers.items():
                    if "key" in k.lower() or "auth" in k.lower():
                        debug_headers[k] = v[:5] + "..." if v else v
                    else:
                        debug_headers[k] = v
                print(f"Headers: {json.dumps(debug_headers)}")
            
            response = requests.post(url, headers=headers, json=data)
            
            if self.debug_mode:
                print(f"Status code: {response.status_code}")
                if response.status_code != 200:
                    print(f"Error response: {response.text[:500]}")
            
            if response.status_code != 200:
                return f"âŒ Error en la consulta: {response.status_code} - {response.text[:100]}"
            
            response_json = response.json()
            
            # Extraer el texto de la respuesta (diferente segÃºn el proveedor)
            if is_deepseek:
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    message = response_json["choices"][0].get("message", {})
                    return message.get("content", "No se recibiÃ³ contenido en la respuesta.")
            else:
                # Extraer para Claude
                if "content" in response_json:
                    for item in response_json.get("content", []):
                        if item.get("type") == "text":
                            return item.get("text", "")
            
            return "âš ï¸ No se pudo extraer texto de la respuesta."
                
        except requests.exceptions.RequestException as e:
            if self.debug_mode:
                print(f"Error de conexiÃ³n: {str(e)}")
                print(traceback.format_exc())
            return f"ðŸš¨ Error en la conexiÃ³n con la API: {str(e)}"
        except Exception as e:
            if self.debug_mode:
                print(f"Error inesperado: {str(e)}")
                print(traceback.format_exc())
            return f"ðŸš¨ Error inesperado: {str(e)}"
    
# En controllers/ia_controller.py, actualizar el método _call_gemini_api

    def _call_gemini_api(self, messages: List[Dict[str, str]]) -> str:
        """Realiza la llamada a la API de Gemini"""
        api_key = self.api_config["clave"]
        
        # URL actualizada - verificar documentación más reciente
        base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        url = f"{base_url}?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Formato actualizado para Gemini
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": gemini_messages,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
                "topP": 0.95,
                "topK": 40
            }
        }
       
        try:
            if self.debug_mode:
                print(f"Enviando consulta a Gemini con {len(messages)} mensajes...")
                print(f"URL: {url[:url.index('?') + 5]}...")  # Ocultar la API key
            
            response = requests.post(url, headers=headers, json=data)
            
            if self.debug_mode:
                print(f"Status code: {response.status_code}")
                if response.status_code != 200:
                    print(f"Error response: {response.text[:500]}")
            
            if response.status_code != 200:
                return f"âŒ Error en la consulta a Gemini: {response.status_code} - {response.text[:100]}"
            
            response_json = response.json()
            
            # Extraer el texto de la respuesta segÃºn el formato de Gemini
            if "candidates" in response_json and len(response_json["candidates"]) > 0:
                candidate = response_json["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            return part["text"]
                
            return "âš ï¸ No se pudo extraer texto de la respuesta de Gemini."
                
        except requests.exceptions.RequestException as e:
            if self.debug_mode:
                print(f"Error de conexiÃ³n con Gemini: {str(e)}")
                print(traceback.format_exc())
            return f"ðŸš¨ Error en la conexiÃ³n con Gemini: {str(e)}"
        except Exception as e:
            if self.debug_mode:
                print(f"Error inesperado con Gemini: {str(e)}")
                print(traceback.format_exc())
            return f"ðŸš¨ Error inesperado con Gemini: {str(e)}"