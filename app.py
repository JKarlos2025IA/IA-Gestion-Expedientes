import os
import streamlit as st
import json  # Para el formato JSON en la vista de documentos
import pandas as pd  # Añadir importación de pandas
from controllers.chat_controller import ChatController
from controllers.ia_controller import IAController
from models.expediente_model import ExpedienteModel
from models.documento_model import DocumentoModel
from config import APIS_DISPONIBLES

# Configuración de la página
st.set_page_config(page_title="IA - Gestión de Expedientes", layout="wide")

# Inicialización de controladores
def init_controllers():
    # Obtener o crear un ID de usuario (simplificado para el ejemplo)
    if 'user_id' not in st.session_state:
        st.session_state.user_id = "usuario_" + os.environ.get("USERNAME", "default")
    
    # Inicializar controlador IA si no existe
    if 'ia_controller' not in st.session_state:
        st.session_state.ia_controller = IAController()
    
    # Inicializar controlador de chat si no existe
    if 'chat_controller' not in st.session_state:
        st.session_state.chat_controller = ChatController(
            api_name=st.session_state.get('selected_api', "Claude"),
            user_id=st.session_state.user_id
        )

# Crear la barra lateral
def crear_sidebar():
    st.sidebar.title("IA - Gestión de Expedientes")
    
    # Menú de navegación - IMPORTANTE: Usamos key="menu_nav" para forzar la actualización
    menu = st.sidebar.radio("Navegación", [
        "Explorar Expedientes", 
        "Chat", 
        "Subir PDF",
        "Historial de Conversaciones"
    ], key="menu_nav")
    
    # Opción para elegir la API de IA
    opcion_ia = st.sidebar.selectbox(
        "Selecciona el modelo de IA", 
        list(APIS_DISPONIBLES.keys()),
        index=list(APIS_DISPONIBLES.keys()).index(st.session_state.get('selected_api', "Claude")),
        key="selector_api"  # Agregar clave única
    )
    
    # Actualizar la API seleccionada si cambia
    if 'selected_api' not in st.session_state or st.session_state.selected_api != opcion_ia:
        st.session_state.selected_api = opcion_ia
        if 'ia_controller' in st.session_state:
            st.session_state.ia_controller.set_api(opcion_ia)
        if 'chat_controller' in st.session_state:
            st.session_state.chat_controller.set_api(opcion_ia)
    
    # Visualización de proyectos en el sidebar
    if 'user_id' in st.session_state:
        # Este componente se podría expandir para mostrar proyectos
        st.sidebar.markdown("---")
        st.sidebar.subheader("Mis Proyectos")
        
        # Ejemplo simplificado - esto se expandiría con datos reales
        proyecto_actual = st.sidebar.selectbox(
            "Proyecto actual:",
            ["General", "Contrataciones 2025", "Casos Laborales", "Normativa TLC"],
            index=0,
            key="selector_proyecto"  # Agregar clave única
        )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("*Proyecto en desarrollo por JKarlos2025IA*")
    
    return menu

# Sección de consulta de expedientes
# Reemplazar la parte de mostrar documentos en la función mostrar_busqueda_expedientes

def mostrar_busqueda_expedientes():
    st.title("Buscar Expedientes")
    
    # Formulario de búsqueda
    numero_expediente = st.text_input("Ingrese el número de expediente:", key="input_expediente")
    
    with st.expander("Búsqueda avanzada", expanded=False):
        tipo_proceso = st.selectbox("Tipo de proceso:", [
            "Todos", "Contratación", "Administrativo", "Recurso", "Otro"
        ], key="select_tipo_proceso")
        
        tema_principal = st.text_input("Tema principal:", key="input_tema")
        
        fechas = st.date_input("Rango de fechas:", [], key="date_rango")
    
    # Botón para ejecutar búsqueda
    if st.button("Buscar", key="btn_buscar"):
        if numero_expediente.strip() == "" and tipo_proceso == "Todos" and tema_principal.strip() == "":
            st.warning("Por favor, ingrese al menos un criterio de búsqueda.")
            return
        
        # Crear modelo de expedientes para realizar la búsqueda
        expediente_model = ExpedienteModel()
        
        if numero_expediente.strip() != "":
            # Búsqueda por número de expediente
            with st.spinner("Buscando expediente..."):
                resultado = expediente_model.get_by_numero(numero_expediente)
                
                if resultado:
                    # Si encontramos el expediente, obtenemos sus documentos
                    documento_model = DocumentoModel()
                    documentos = documento_model.get_by_expediente_id(resultado["id"])
                    
                    # Mostrar resultados
                    st.success("Expediente encontrado:")
                    
                    # Visualización del expediente usando tabs
                    tab1, tab2 = st.tabs(["Información General", "Documentos"])
                    
                    with tab1:
                        # Mostrar información general del expediente
                        st.subheader(f"Expediente: {resultado.get('numero_expediente')}")
                        
                        # Crear columnas para visualización
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Fecha de creación:** {resultado.get('fecha_creacion')}")
                            st.markdown(f"**Tipo de proceso:** {resultado.get('tipo_proceso')}")
                            st.markdown(f"**Sección:** {resultado.get('seccion')}")
                        
                        with col2:
                            st.markdown(f"**Modalidad:** {resultado.get('modalidad')}")
                            st.markdown(f"**Tema principal:** {resultado.get('tema_principal')}")
                            if 'area_solicitante' in resultado:
                                st.markdown(f"**Área solicitante:** {resultado.get('area_solicitante')}")
                    
                    with tab2:
                        # Mostrar documentos asociados
                        if documentos:
                            st.subheader(f"Documentos ({len(documentos)})")
                            
                            # OPCIÓN 1: Vista en lista desplegable con contenido detallado
                            doc_names = [doc.get('nombre_archivo', f'Documento {i+1}') for i, doc in enumerate(documentos)]
                            selected_doc_name = st.selectbox("Seleccione un documento para ver detalles:", 
                                                     doc_names, key="doc_selector")
                            
                            # Obtener el índice del documento seleccionado
                            selected_idx = doc_names.index(selected_doc_name)
                            doc = documentos[selected_idx]
                            
                            # Mostrar detalles del documento seleccionado
                            st.markdown("### Detalles del documento")
                            st.markdown(f"**Tipo:** {doc.get('tipo_documento', 'No especificado')}")
                            st.markdown(f"**Archivo:** {doc.get('nombre_archivo', 'Sin nombre')}")
                            st.markdown(f"**Fecha de subida:** {doc.get('fecha_subida', 'No registrada')}")
                            
                            # Mostrar contenido en un área de texto
                            if 'contenido' in doc and doc['contenido']:
                                st.markdown("### Contenido")
                                st.text_area("", value=doc['contenido'], height=300, key="doc_content", label_visibility="collapsed")
                                
                            # OPCIÓN 2: Vista JSON (Alternativa)
                            with st.expander("Ver todos los documentos en formato JSON"):
                                st.code(json.dumps(documentos, indent=2, ensure_ascii=False), language="json")
                        else:
                            st.info("Este expediente no tiene documentos asociados.")
                else:
                    st.error("No se encontró el expediente.")
        else:
            # Búsqueda avanzada (simplificada para el ejemplo)
            st.info("Implementación de búsqueda avanzada pendiente.")# Sección de Chat con IA
def mostrar_chat():
    st.title("Chat con IA sobre Expedientes")
    
    # Verificar si tenemos el controlador de chat inicializado
    if 'chat_controller' not in st.session_state:
        st.session_state.chat_controller = ChatController(
            api_name=st.session_state.get('selected_api', "Claude"),
            user_id=st.session_state.user_id
        )
    
    # Obtener o crear una conversación actual
    if 'current_conversation_id' not in st.session_state:
        # Inicia una nueva conversación
        conv_id = st.session_state.chat_controller.create_conversation("Nueva consulta legal")
        st.session_state.current_conversation_id = conv_id
    
    # Mostrar historial de mensajes
    if st.session_state.current_conversation_id:
        mensajes = st.session_state.chat_controller.get_conversation_history(
            st.session_state.current_conversation_id
        )
        
        # Mostrar los mensajes en la interfaz
        mensaje_container = st.container()
        with mensaje_container:
            for mensaje in mensajes:
                if mensaje["role"] == "user":
                    st.markdown(f"**Tú:** {mensaje['content']}")
                else:
                    st.markdown(f"**Asistente:** {mensaje['content']}")
    
    # Campo de entrada para nueva consulta
    consulta = st.text_area("Escribe tu pregunta sobre los expedientes:", 
                        placeholder="Ejemplo: Búscame expedientes relacionados con contrataciones de la Dirección de Evaluación...",
                        key="input_consulta")

    # Crear tres columnas para los botones
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("Enviar", use_container_width=True, key="btn_enviar"):
            if consulta.strip() == "":
                st.warning("Por favor, escribe una consulta.")
                return
            
            # Procesar la consulta
            with st.spinner("Buscando información y generando respuesta..."):
                try:
                    result = st.session_state.chat_controller.process_query(
                        consulta, 
                        st.session_state.current_conversation_id
                    )
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # Recargar la página para mostrar los nuevos mensajes
                        st.rerun()  # Aquí es donde se hace el cambio
                except Exception as e:
                    st.error(f"Error al procesar la consulta: {str(e)}")
    
    with col2:
        if st.button("Nueva Conversación", use_container_width=True, key="btn_nueva_conv"):
            # Crear una nueva conversación
            try:
                conv_id = st.session_state.chat_controller.create_conversation("Nueva consulta legal")
                st.session_state.current_conversation_id = conv_id
                st.rerun()  # Aquí es donde se hace el cambio
            except Exception as e:
                st.error(f"Error al crear nueva conversación: {str(e)}")

# Sección para subir PDF
def subir_pdf():
    st.title("Subir Documentos PDF")
    
    # Campos para el formulario
    numero_expediente = st.text_input("Número de expediente:", key="input_pdf_expediente")
    
    # Verificar si el expediente existe cuando se ingresa un número
    expediente_existe = False
    expediente_id = None
    
    if numero_expediente.strip():
        # Verificar si el expediente existe
        expediente_model = ExpedienteModel()
        expediente = expediente_model.get_by_numero(numero_expediente)
        
        if expediente:
            expediente_existe = True
            expediente_id = expediente["id"]
            st.success(f"✅ Expediente {numero_expediente} encontrado.")
        else:
            st.warning(f"⚠️ El expediente {numero_expediente} no existe en el sistema.")
            crear_expediente = st.checkbox("Crear este expediente nuevo", value=True, 
                                         help="Marque esta casilla para crear un nuevo expediente con este número")
    
    # Widget para subir archivo
    archivo = st.file_uploader("Selecciona un archivo PDF", type=["pdf"], key="upload_pdf")
    
    if archivo:
        # Mostrar información del archivo
        st.success(f"Archivo {archivo.name} subido correctamente.")
        
        # Procesar el PDF para extraer texto
        with st.spinner("Extrayendo texto del PDF..."):
            try:
                # Leer el contenido del archivo
                pdf_bytes = archivo.read()
                
                # Extraer texto usando PyMuPDF
                import fitz  # PyMuPDF
                import tempfile
                import io
                
                # Crear archivo temporal con los bytes
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                    temp_file.write(pdf_bytes)
                    temp_path = temp_file.name
                
                texto_extraido = ""
                try:
                    with fitz.open(temp_path) as doc:
                        texto_extraido = "\n".join([page.get_text() for page in doc])
                except Exception as e:
                    st.warning(f"No se pudo extraer texto del PDF: {str(e)}")
                    texto_extraido = "[No se pudo extraer texto automáticamente]"
                
                # Mostrar y permitir editar el texto extraído
                st.subheader("Texto extraído del documento")
                texto_editado = st.text_area("Revisa y edita el texto si es necesario:", 
                                           value=texto_extraido, 
                                           height=300,
                                           key="texto_extraido")
                
                # Tipo de documento
                tipo_documento = st.selectbox(
                    "Tipo de documento:",
                    ["Oficio", "Memorando", "Informe", "Carta", "Contrato", 
                     "Proveído", "Hoja de Envío", "TDR", "Información Complementaria", "Anexo"],
                    key="select_tipo_doc"
                )
                
                # Si el expediente no existe, mostrar formulario para crearlo
                if not expediente_existe:
                    st.subheader("Datos del nuevo expediente")
                    
                    from datetime import date
                    fecha_creacion = st.date_input("Fecha de creación:", value=date.today(), key="fecha_creacion")
                    tipo_proceso = st.selectbox("Tipo de proceso:", 
                                              ["Contratación", "Administrativo", "Recurso", "Evaluación", "Otro"],
                                              key="tipo_proceso")
                    modalidad = st.text_input("Modalidad:", value="Pendiente", key="modalidad")
                    seccion = st.text_input("Sección:", value="Pendiente", key="seccion")
                    tema_principal = st.text_input("Tema principal:", value="Pendiente", key="tema_principal")
                    area_solicitante = st.text_input("Área solicitante:", value="Pendiente", key="area_solicitante")
                    
                    # NUEVO: Campo estado
                    estado = st.selectbox("Estado del expediente:", 
                                        ["Activo", "En proceso", "Finalizado", "Archivado", "Suspendido"],
                                        key="estado_expediente")
                
                # Botón para guardar
                if st.button("Guardar documento", key="btn_guardar_doc"):
                    if numero_expediente.strip() == "":
                        st.error("Por favor, ingrese un número de expediente.")
                        return
                    
                    # Crear el expediente si no existe
                    if not expediente_existe:
                        with st.spinner("Creando nuevo expediente..."):
                            # Crear nuevo expediente con los datos del formulario
                            datos_expediente = {
                                "numero_expediente": numero_expediente,
                                "fecha_creacion": fecha_creacion.isoformat(),
                                "tipo_proceso": tipo_proceso,
                                "modalidad": modalidad,
                                "seccion": seccion,
                                "tema_principal": tema_principal,
                                "area_solicitante": area_solicitante,
                                "estado": estado  # NUEVO: Incluir campo estado
                            }
                            
                            print(f"Datos para crear expediente: {datos_expediente}")
                            expediente_result = expediente_model.create(datos_expediente)
                            
                            if expediente_result:
                                st.success(f"✅ Expediente {numero_expediente} creado correctamente.")
                                expediente_id = expediente_result["id"]
                            else:
                                st.error("❌ No se pudo crear el expediente. Verifique los datos e intente nuevamente.")
                                # Mostrar información detallada para depuración
                                st.expander("Detalles del error (para administradores)", expanded=False).code(
                                    f"Datos enviados: {datos_expediente}"
                                )
                                return
                    
                    # Guardar el documento
                    if expediente_id:
                        with st.spinner("Guardando documento..."):
                            documento_model = DocumentoModel()
                            from datetime import datetime
                            
                            documento_data = {
                                "expediente_id": expediente_id,
                                "nombre_archivo": archivo.name,
                                "tipo_documento": tipo_documento,
                                "contenido": texto_editado,
                                "fecha_subida": datetime.now().isoformat()
                            }
                            
                            resultado = documento_model.create(documento_data)
                            
                            if resultado:
                                st.success(f"✅ Documento '{archivo.name}' guardado exitosamente en el expediente {numero_expediente}.")
                                
                                # Mostrar un botón para ver el expediente
                                if st.button("Ver expediente", key="btn_ver_expediente"):
                                    st.session_state.menu_nav = "Explorar Expedientes"
                                    st.session_state.buscar_expediente = numero_expediente
                                    st.rerun()
                            else:
                                st.error("❌ Error al guardar el documento en la base de datos.")
                    else:
                        st.error("❌ No se encontró un ID de expediente válido para guardar el documento.")
                        
            except Exception as e:
                st.error(f"❌ Error al procesar el documento: {str(e)}")
                st.expander("Detalles técnicos", expanded=False).code(str(e))# Añadir esta función a app.py y modificar el menú para incluir esta opción

def procesar_lote_pdfs():
    st.title("Procesamiento por Lotes de Documentos PDF")
    
    # Campo para seleccionar el expediente
    numero_expediente = st.text_input("Número de expediente:", key="batch_expediente_numero")
    
    # Verificación de existencia del expediente
    expediente_existe = False
    expediente_id = None
    crear_expediente = False
    
    if numero_expediente.strip():
        # Verificar si el expediente existe
        expediente_model = ExpedienteModel()
        expediente = expediente_model.get_by_numero(numero_expediente)
        
        if expediente:
            expediente_existe = True
            expediente_id = expediente["id"]
            st.success(f"✅ Expediente {numero_expediente} encontrado.")
        else:
            st.warning(f"⚠️ El expediente {numero_expediente} no existe en el sistema.")
            crear_expediente = st.checkbox("Crear este expediente al procesar", value=True)
    
    # Widget para subir múltiples archivos
    archivos = st.file_uploader("Selecciona archivos PDF (puedes seleccionar varios)", 
                              type=["pdf"], accept_multiple_files=True, key="batch_upload")
    
    if archivos:
        st.success(f"Se han subido {len(archivos)} archivos.")
        
        # Mostrar archivos subidos
        with st.expander(f"Archivos subidos ({len(archivos)})", expanded=True):
            for i, archivo in enumerate(archivos):
                st.text(f"{i+1}. {archivo.name} ({archivo.size} bytes)")
        
        # Botón para procesar archivos
        if st.button("Procesar Archivos", key="btn_procesar_lote", 
                    disabled=(not numero_expediente.strip() or (not expediente_existe and not crear_expediente))):
            
            if not numero_expediente.strip():
                st.error("Por favor, ingrese un número de expediente.")
                return
            
            # Crear expediente si no existe
            if not expediente_existe and crear_expediente:
                with st.spinner("Creando nuevo expediente..."):
                    # Fecha actual como fecha de creación
                    from datetime import date
                    
                    nuevo_expediente = {
                        "numero_expediente": numero_expediente,
                        "fecha_creacion": date.today().isoformat(),
                        "tipo_proceso": "Pendiente",
                        "modalidad": "Pendiente",
                        "seccion": "Pendiente",
                        "tema_principal": "Pendiente",
                        "area_solicitante": "Pendiente",
                        "estado": "Activo"  # NUEVO: Incluir campo estado
                    }
                    
                    expediente_result = expediente_model.create(nuevo_expediente)
                    
                    if expediente_result:
                        st.success(f"Se ha creado el nuevo expediente {numero_expediente}")
                        expediente_id = expediente_result["id"]
                        expediente_existe = True
                    else:
                        st.error("No se pudo crear el nuevo expediente.")
                        return
            
            # Procesar cada archivo
            resultados_procesamiento = []
            
            # Barra de progreso
            progress_bar = st.progress(0)
            
            for i, archivo in enumerate(archivos):
                # Actualizar progreso
                progress_bar.progress((i+1)/len(archivos))
                
                with st.spinner(f"Procesando archivo {i+1}/{len(archivos)}: {archivo.name}"):
                    try:
                        # Leer archivo
                        pdf_bytes = archivo.read()
                        
                        # Extraer texto del PDF
                        import fitz  # PyMuPDF
                        import tempfile
                        import re
                        
                        # Guardar los bytes en un archivo temporal
                        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                            temp_file.write(pdf_bytes)
                            temp_path = temp_file.name
                        
                        # Extraer texto con PyMuPDF
                        texto_extraido = ""
                        try:
                            with fitz.open(temp_path) as doc:
                                texto_extraido = "\n".join([page.get_text() for page in doc])
                        except Exception as e:
                            texto_extraido = "[No se pudo extraer texto]"
                        
                        # Detectar tipo de documento basado en nombre o contenido
                        tipo_detectado = "Pendiente"
                        patrones = {
                            "Oficio": r"(?i)\bOFICIO\b",
                            "Memorando": r"(?i)\bMEMORANDO\b",
                            "Informe": r"(?i)\bINFORME\b",
                            "Carta": r"(?i)\bCARTA\b",
                            "Contrato": r"(?i)\bCONTRATO\b",
                            "Proveído": r"(?i)\bPROVE[IÍ]DO\b",
                            "Hoja de Envío": r"(?i)\bHOJA\S+DE\S+ENV[IÍ]O\b",
                            "TDR": r"(?i)\bTDR\b",
                            "Información Complementaria": r"(?i)\bINFORMACIÓN\s+COMPLEMENTARIA\b",
                            "Anexo": r"(?i)\bANEXO\b"
                        }
                        
                        for tipo, patron in patrones.items():
                            if re.search(patron, texto_extraido) or re.search(patron, archivo.name):
                                tipo_detectado = tipo
                                break
                        
                        # Añadir a resultados
                        resultados_procesamiento.append({
                            "nombre": archivo.name,
                            "texto_extraido": texto_extraido[:500] + "..." if len(texto_extraido) > 500 else texto_extraido,
                            "tipo_detectado": tipo_detectado,
                            "pdf_bytes": pdf_bytes  # Guardar los bytes para procesamiento posterior
                        })
                        
                    except Exception as e:
                        st.error(f"Error al procesar {archivo.name}: {str(e)}")
                        resultados_procesamiento.append({
                            "nombre": archivo.name,
                            "error": str(e)
                        })
            
            # Mostrar resultados para revisión
            st.subheader("Revisión de documentos procesados")
            st.info("Revise la información extraída y ajuste lo necesario antes de guardar.")
            
            # DataFrame para mostrar resultados
            documentos_para_guardar = []
            
            # Crear tabs para cada documento
            tabs = st.tabs([f"Doc {i+1}: {res['nombre']}" for i, res in enumerate(resultados_procesamiento)])
            
            for i, (tab, resultado) in enumerate(zip(tabs, resultados_procesamiento)):
                with tab:
                    if "error" in resultado:
                        st.error(f"Error: {resultado['error']}")
                        continue
                    
                    st.markdown(f"### {resultado['nombre']}")
                    
                    # Selección de tipo de documento
                    tipo_doc = st.selectbox("Tipo de documento:", 
                                          ["Oficio", "Memorando", "Informe", "Carta", "Contrato", 
                                          "Proveído", "Hoja de Envío", "TDR", "Información Complementaria", "Anexo"],
                                          index=["Oficio", "Memorando", "Informe", "Carta", "Contrato", 
                                                "Proveído", "Hoja de Envío", "TDR", "Información Complementaria", "Anexo"]
                                                .index(resultado["tipo_detectado"]) if resultado["tipo_detectado"] in ["Oficio", "Memorando", "Informe", "Carta", "Contrato", 
                                                                                                                    "Proveído", "Hoja de Envío", "TDR", "Información Complementaria", "Anexo"] else 0,
                                          key=f"tipo_doc_{i}")
                    
                    # Vista previa del texto extraído
                    st.markdown("#### Contenido extraído")
                    texto_area = st.text_area("Editar contenido si es necesario:", 
                                             value=resultado["texto_extraido"], 
                                             height=200, 
                                             key=f"texto_{i}")
                    
                    # Checkbox para incluir este documento
                    incluir = st.checkbox("Incluir este documento", value=True, key=f"incluir_{i}")
                    
                    if incluir:
                        documentos_para_guardar.append({
                            "nombre": resultado["nombre"],
                            "tipo": tipo_doc,
                            "contenido": texto_area,
                            "pdf_bytes": resultado["pdf_bytes"]
                        })
            
            # Botón para guardar todos los documentos seleccionados
            if st.button("Guardar todos los documentos seleccionados", key="btn_guardar_todos"):
                if not documentos_para_guardar:
                    st.warning("No hay documentos seleccionados para guardar.")
                    return
                
                with st.spinner(f"Guardando {len(documentos_para_guardar)} documentos..."):
                    documento_model = DocumentoModel()
                    from datetime import datetime
                    
                    documentos_guardados = 0
                    for doc in documentos_para_guardar:
                        try:
                            # Datos del documento
                            documento_data = {
                                "expediente_id": expediente_id,
                                "nombre_archivo": doc["nombre"],
                                "tipo_documento": doc["tipo"],
                                "contenido": doc["contenido"],
                                "fecha_subida": datetime.now().isoformat()
                            }
                            
                            # Guardar documento
                            resultado = documento_model.create(documento_data)
                            
                            if resultado:
                                documentos_guardados += 1
                            
                        except Exception as e:
                            st.error(f"Error al guardar {doc['nombre']}: {str(e)}")
                    
                    if documentos_guardados > 0:
                        st.success(f"Se guardaron {documentos_guardados} documentos en el expediente {numero_expediente}.")
                        
                        # Botón para ver el expediente
                        if st.button("Ver expediente", key="btn_ver_expediente_batch"):
                            # Cambiar a la página de expedientes y buscar este
                            st.session_state.menu_nav = "Explorar Expedientes"
                            # Guardar el número para buscarlo
                            st.session_state.buscar_expediente = numero_expediente
                            st.rerun()
                    else:
                        st.error("No se pudo guardar ningún documento.")

# Asegúrate de que esta función esté en app.py
def mostrar_historial_conversaciones():
    st.title("Historial de Conversaciones")
    
    # Verificar si tenemos el controlador de chat inicializado
    if 'chat_controller' not in st.session_state:
        st.session_state.chat_controller = ChatController(
            api_name=st.session_state.get('selected_api', "Claude"),
            user_id=st.session_state.user_id
        )
    
    # Obtener todas las conversaciones del usuario
    try:
        conversaciones = st.session_state.chat_controller.get_user_conversations()
        
        if not conversaciones:
            st.info("No tienes conversaciones guardadas.")
            return
        
        # Mostrar conversaciones
        st.subheader(f"Tus conversaciones ({len(conversaciones)})")
        
        for i, conv in enumerate(conversaciones):
            with st.expander(f"{conv.get('title', 'Conversación')} - {conv.get('created_at', 'Fecha desconocida')[:10]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Continuar conversación", key=f"continue_{i}"):
                        st.session_state.current_conversation_id = conv['id']
                        st.session_state.chat_controller.set_conversation(conv['id'])
                        # Cambiar a la página de chat
                        st.session_state.menu_nav = "Chat"
                        st.rerun()
                
                with col2:
                    if st.button("Eliminar", key=f"delete_{i}"):
                        if st.session_state.chat_controller.delete_conversation(conv['id']):
                            st.success("Conversación eliminada correctamente.")
                            st.rerun()
                        else:
                            st.error("Error al eliminar la conversación.")
                
                # Mostrar resumen de mensajes
                mensajes = st.session_state.chat_controller.get_conversation_history(conv['id'])
                if mensajes:
                    st.markdown("### Resumen")
                    for j, msg in enumerate(mensajes[:3]):  # Mostrar solo primeros mensajes
                        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content'][:100]}..." if len(msg['content']) > 100 else f"**{msg['role'].capitalize()}:** {msg['content']}")
                    
                    if len(mensajes) > 3:
                        st.info(f"... y {len(mensajes) - 3} mensajes más.")
    except Exception as e:
        st.error(f"Error al cargar conversaciones: {str(e)}")
        st.code(str(e))  # Mostrar el error para depuración# Función principal
def main():
    # Inicializar controladores
    init_controllers()
    
    # Crear barra lateral y obtener menú seleccionado
    menu = crear_sidebar()
    
    # Guardar el menú en session_state para navegación
    if 'menu_nav' not in st.session_state:
        st.session_state.menu_nav = menu
    elif st.session_state.menu_nav != menu:
        # El menú cambió, actualizar
        menu = st.session_state.menu_nav
    
    # Mostrar la sección seleccionada - Con manejo de errores
    try:
        if menu == "Explorar Expedientes":
            mostrar_busqueda_expedientes()
        elif menu == "Chat":
            mostrar_chat()
        elif menu == "Subir PDF":
            subir_pdf()
        elif menu == "Historial de Conversaciones":
            mostrar_historial_conversaciones()
        else:
            st.error(f"Menú no reconocido: {menu}")
    except Exception as e:
        st.error(f"Error al cargar la sección {menu}: {str(e)}")
        st.code(str(e))  # Mostrar el error para depuración

# Estilos CSS para la aplicación
def apply_custom_css():
    st.markdown("""
        <style>
        body { background-color: #1e1e1e; color: white; font-family: 'Arial', sans-serif; }
        .stApp { background-color: #1e1e1e; }
        .css-1d391kg, .css-qrbaxs { background-color: #1e1e1e; color: white; font-size: 18px; }
        .css-10trblm { color: white; }
        .css-1lcbmhc { background-color: #252525 !important; }
        .css-1hynsf2 { font-size: 18px !important; font-weight: bold; color: #FFD700 !important; }
        .css-16idsys { font-size: 16px !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    apply_custom_css()
    main()