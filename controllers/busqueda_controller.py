# controllers/busqueda_controller.py
from typing import Dict, List, Any, Optional
from models.expediente_model import ExpedienteModel
from models.documento_model import DocumentoModel

class BusquedaController:
    def __init__(self):
        self.expediente_model = ExpedienteModel()
        self.documento_model = DocumentoModel()
        # Límites para resultados
        self.max_expedientes = 5
        self.max_documentos = 7
        self.max_normativas = 3
    
    def search(self, keywords: List[str], expediente_numbers: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Realiza una búsqueda completa en la base de datos
        :param keywords: Lista de palabras clave
        :param expediente_numbers: Lista de números de expediente específicos
        :return: Diccionario con resultados agrupados
        """
        results = {
            "expedientes": [],
            "documentos": [],
            "normativas": []
        }
        
        # 1. Si hay números de expediente específicos, buscarlos primero
        if expediente_numbers and len(expediente_numbers) > 0:
            for num_exp in expediente_numbers:
                expediente = self.expediente_model.get_by_numero(num_exp)
                if expediente:
                    results["expedientes"].append(expediente)
        
        # 2. Buscar expedientes por palabras clave
        if keywords and len(keywords) > 0:
            keyword_expedientes = self.expediente_model.search_by_keywords(keywords, self.max_expedientes)
            # Combinar con los expedientes ya encontrados sin duplicar
            existing_ids = {exp["id"] for exp in results["expedientes"]}
            for exp in keyword_expedientes:
                if exp["id"] not in existing_ids:
                    results["expedientes"].append(exp)
                    existing_ids.add(exp["id"])
            
            # Limitar la cantidad total de expedientes
            results["expedientes"] = results["expedientes"][:self.max_expedientes]
        
        # 3. Buscar documentos relacionados con los expedientes encontrados
        expediente_ids = [exp["id"] for exp in results["expedientes"]]
        for exp_id in expediente_ids:
            documentos = self.documento_model.get_by_expediente_id(exp_id)
            if documentos:
                # Enriquecer documentos con información del expediente
                documentos = self.documento_model.enrich_documents_with_expediente_info(documentos)
                results["documentos"].extend(documentos)
        
        # 4. Buscar documentos directamente por contenido
        if keywords and len(keywords) > 0:
            content_docs = self.documento_model.search_by_content(keywords)
            # Enriquecer con información de expedientes
            content_docs = self.documento_model.enrich_documents_with_expediente_info(content_docs)
            
            # Combinar con los documentos ya encontrados sin duplicar
            existing_ids = {doc["id"] for doc in results["documentos"]}
            for doc in content_docs:
                if doc["id"] not in existing_ids:
                    results["documentos"].append(doc)
                    existing_ids.add(doc["id"])
        
        # 5. Limitar la cantidad total de documentos
        results["documentos"] = results["documentos"][:self.max_documentos]
        
        # 6. Buscar en normativas (implementar según necesidades)
        self._search_normativas(keywords, results)
        
        return results
    
    def _search_normativas(self, keywords: List[str], results: Dict[str, Any]) -> None:
        """
        Busca en las tablas de normativas
        :param keywords: Lista de palabras clave 
        :param results: Diccionario donde se añadirán los resultados
        """
        # Esta función podría consultar a un cliente Supabase directamente
        # Simulamos un resultado para el ejemplo
        from utils.supabase_client import get_supabase_client
        
        if not keywords:
            return
            
        tablas_normativa = [
            "normativa_anexos", "normativa_articulos", "normativa_disposiciones", 
            "normativa_documentos", "normativa_estructura", "normativa_literales", 
            "normativa_numerales", "normativa_referencias"
        ]
        
        supabase = get_supabase_client()
        
        for tabla in tablas_normativa:
            try:
                # Verificar si la tabla existe
                muestra = supabase.table(tabla).select("*").limit(1).execute()
                
                if muestra.data:
                    # Obtener columnas de la tabla
                    columnas = list(muestra.data[0].keys())
                    columnas_texto = [col for col in columnas if col not in ["id", "created_at", "updated_at"]]
                    
                    for columna in columnas_texto:
                        for palabra in keywords:
                            try:
                                response = supabase.table(tabla).select("*").ilike(columna, f"%{palabra}%").limit(2).execute()
                                if response.data:
                                    results["normativas"].append({
                                        "tabla": tabla,
                                        "columna": columna,
                                        "palabra_clave": palabra,
                                        "datos": response.data
                                    })
                            except Exception as e:
                                # Error específico por columna - continuamos con la siguiente
                                pass
            except Exception as e:
                # Error con la tabla - continuamos con la siguiente
                pass
        
        # Limitar la cantidad total de grupos de normativas
        results["normativas"] = results["normativas"][:self.max_normativas]