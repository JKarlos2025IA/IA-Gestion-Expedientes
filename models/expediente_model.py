# models/expediente_model.py
from utils.supabase_client import get_supabase_client
from typing import Dict, List, Optional, Any

class ExpedienteModel:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "expedientes"
    
    def get_by_numero(self, numero_expediente: str) -> Optional[Dict[str, Any]]:
        """Obtiene un expediente por su número"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("numero_expediente", numero_expediente)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al obtener expediente por número: {e}")
            return None
    
    def get_by_id(self, expediente_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un expediente por su ID"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", expediente_id)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al obtener expediente por ID: {e}")
            return None
    
    def search_by_keywords(self, keywords: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """Busca expedientes que contengan las palabras clave en varios campos"""
        results = []
        fields = ["numero_expediente", "tipo_proceso", "tema_principal", "area_solicitante", "seccion"]
        
        for field in fields:
            for keyword in keywords:
                try:
                    response = (
                        self.supabase.table(self.table_name)
                        .select("*")
                        .ilike(field, f"%{keyword}%")
                        .limit(limit)
                        .execute()
                    )
                    
                    if response.data:
                        results.extend(response.data)
                except Exception as e:
                    print(f"Error al buscar en {field} con palabra clave '{keyword}': {e}")
        
        # Eliminar duplicados por ID
        unique_results = {}
        for exp in results:
            unique_results[exp["id"]] = exp
        
        return list(unique_results.values())
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo expediente"""
        try:
            response = self.supabase.table(self.table_name).insert(data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al crear expediente: {e}")
            return None
    
    def update(self, expediente_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un expediente existente"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .update(data)
                .eq("id", expediente_id)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error al actualizar expediente: {e}")
            return None