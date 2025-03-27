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
    
    # En models/expediente_model.py
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo expediente con mejor manejo de errores"""
        try:
            # Verificar y limpiar datos
            cleaned_data = {}
            for key, value in data.items():
                if key in ["numero_expediente", "fecha_creacion", "tipo_proceso", 
                          "modalidad", "seccion", "tema_principal", "area_solicitante", "estado"]:
                    cleaned_data[key] = str(value) if value is not None else ""
            
            # Añadir estado por defecto si no está presente
            if "estado" not in cleaned_data or not cleaned_data["estado"]:
                cleaned_data["estado"] = "Activo"
            
            print(f"Intentando crear expediente con datos: {cleaned_data}")
            
            # Intentar insertar con manejo de errores detallado
            try:
                response = self.supabase.table(self.table_name).insert(cleaned_data).execute()
                
                if response.data:
                    print(f"Expediente creado correctamente: {response.data}")
                    return response.data[0]
                else:
                    print(f"No se obtuvo respuesta al crear expediente: {response}")
                    return None
            except Exception as insert_error:
                print(f"Error específico al insertar en Supabase: {insert_error}")
                if hasattr(insert_error, 'response'):
                    print(f"Código de respuesta: {insert_error.response.status_code}")
                    print(f"Texto de respuesta: {insert_error.response.text}")
                return None
                
        except Exception as e:
            print(f"Error general al crear expediente: {e}")
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