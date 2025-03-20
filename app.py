import os
import streamlit as st
from supabase_client import buscar_expediente_completo
from llamadas_ia import consulta_claude
from config import APIS_DISPONIBLES, obtener_api
print("Usando API Key en app.py:", os.environ.get("CLAUDE_API_KEY", "NO ENCONTRADA"))
# Configuración de la página
st.set_page_config(page_title="IA - Gestión de Expedientes", layout="wide")

# Crear la barra lateral
st.sidebar.title("IA - Gestión de Expedientes")
menu = st.sidebar.radio("Navegación", ["Explorar Expedientes", "Chat", "Subir PDF"])

# Opción para elegir la API de IA
opcion_ia = st.sidebar.selectbox("Selecciona el modelo de IA", list(APIS_DISPONIBLES.keys()))

# Sección de consulta de expedientes
def mostrar_busqueda_expedientes():
    st.title("Buscar Expedientes")
    numero_expediente = st.text_input("Ingrese el número de expediente:")

    if st.button("Buscar"):
        if numero_expediente.strip() == "":
            st.warning("Por favor, ingrese un número de expediente.")
            return
        
        resultado = buscar_expediente_completo(numero_expediente)
        
        if resultado:
            st.success("Expediente encontrado:")
            st.json(resultado)
        else:
            st.error("No se encontró el expediente.")

# Sección de Chat con IA
def mostrar_chat():
    st.title("Chat con IA")
    consulta = st.text_area("Escribe tu pregunta sobre los expedientes:")

    if st.button("Consultar"):
        api_seleccionada = obtener_api(opcion_ia)

        if api_seleccionada:
            if opcion_ia == "Claude":
                respuesta = consulta_claude(consulta)
            else:
                respuesta = "⚠️ Modelo no reconocido o aún no implementado."
        else:
            respuesta = "⚠️ No se ha configurado correctamente la API seleccionada."

        st.write("Respuesta de la IA:", respuesta)

# Sección para subir PDF
def subir_pdf():
    st.title("Subir Documentos PDF")
    archivo = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

    if archivo:
        st.success(f"Archivo {archivo.name} subido correctamente.")

# Mostrar la sección seleccionada
if menu == "Explorar Expedientes":
    mostrar_busqueda_expedientes()
elif menu == "Chat":
    mostrar_chat()
elif menu == "Subir PDF":
    subir_pdf()

# Mensaje de bienvenida
st.sidebar.markdown("---")
st.sidebar.markdown("*Proyecto en desarrollo por JKarlos2025IA*")

# Estilos CSS para fondo oscuro
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
