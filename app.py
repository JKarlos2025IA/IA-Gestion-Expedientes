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
    archivo = st.file_uploader("Selecciona un archivo PDF", type=["pdf"], key="upload_pdf")
    
    if archivo:
        # Mostrar información del archivo
        st.success(f"Archivo {archivo.name} subido correctamente.")
        
        # Mostrar vista previa (simplificada)
        st.subheader("Vista previa del documento")
        st.info("Vista previa no disponible. El contenido se procesará al guardar.")
        
        # Opcional: Tipo de documento
        tipo_documento = st.selectbox(
            "Tipo de documento:",
            ["Oficio", "Memorando", "Informe", "Carta", "Contrato", 
             "Proveído", "Hoja de Envío", "TDR", "Información Complementaria", "Anexo"],
            key="select_tipo_doc"
        )
        
        if st.button("Guardar documento", key="btn_guardar_doc"):
            if numero_expediente.strip() == "":
                st.error("Por favor, ingrese un número de expediente.")
                return
            
            # Aquí se procesaría y guardaría el documento
            # Esta implementación se completaría con el procesador de PDFs
            st.success(f"Documento '{archivo.name}' guardado exitosamente en el expediente {numero_expediente}.")

# Sección para ver historial de conversaciones
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
                        st.rerun()  # Aquí es donde se hace el cambio
                                    
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
                    for j, msg in enumerate(mensajes[:3]):  # Mostrar solo los primeros 3 mensajes
                        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content'][:100]}..." if len(msg['content']) > 100 else f"**{msg['role'].capitalize()}:** {msg['content']}")
                    
                    if len(mensajes) > 3:
                        st.info(f"... y {len(mensajes) - 3} mensajes más.")
    except Exception as e:
        st.error(f"Error al cargar conversaciones: {str(e)}")
        st.code(str(e))  # Mostrar el error para depuración

# Función principal
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