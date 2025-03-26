# models/documento_model.py
from utils.supabase_client import get_supabase_client
from typing import Dict, List, Optional, Any

class DocumentoModel:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "documentos_expediente"
    
    def get_by_id(self, documento_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un documento por su ID"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", documento_id)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al obtener documento por ID: {e}")
            return None
    
    def get_by_expediente_id(self, expediente_id: int) -> List[Dict[str, Any]]:
        """Obtiene todos los documentos asociados a un expediente"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("expediente_id", expediente_id)
                .execute()
            )
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al obtener documentos por expediente_id: {e}")
            return []
    
    def search_by_content(self, keywords: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """Busca documentos que contengan las palabras clave en su contenido"""
        results = []
        
        for keyword in keywords:
            try:
                response = (
                    self.supabase.table(self.table_name)
                    .select("*")
                    .ilike("contenido", f"%{keyword}%")
                    .limit(limit)
                    .execute()
                )
                
                if response.data:
                    results.extend(response.data)
            except Exception as e:
                print(f"Error al buscar en contenido con palabra clave '{keyword}': {e}")
        
        # Eliminar duplicados por ID
        unique_results = {}
        for doc in results:
            unique_results[doc["id"]] = doc
        
        return list(unique_results.values())
    
    def search_by_tipo_documento(self, tipo: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca documentos por tipo de documento"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .ilike("tipo_documento", f"%{tipo}%")
                .limit(limit)
                .execute()
            )
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al buscar documentos por tipo: {e}")
            return []
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo documento"""
        try:
            response = self.supabase.table(self.table_name).insert(data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al crear documento: {e}")
            return None
    
    def update(self, documento_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un documento existente"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .update(data)
                .eq("id", documento_id)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al actualizar documento: {e}")
            return None
    
    def enrich_documents_with_expediente_info(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enriquece la lista de documentos con información de sus expedientes"""
        from models.expediente_model import ExpedienteModel
        expediente_model = ExpedienteModel()
        
        for doc in documents:
            if "expediente_id" in doc:
                expediente = expediente_model.get_by_id(doc["expediente_id"])
                if expediente:
                    doc["expediente_numero"] = expediente.get("numero_expediente", "")
                    doc["expediente_tipo"] = expediente.get("tipo_proceso", "")
        
        return documents