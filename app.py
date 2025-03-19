import streamlit as st
from supabase_client import buscar_expediente_completo
st.set_page_config(page_title="IA - Gestiión de Expedientes", page_icon="ðŸ“‚", layout="wide")

st.title("Buscar Expedientes")

numero_expediente = st.text_input("Ingrese el número de expediente:")

if st.button("Buscar"):
    resultado = buscar_expediente_completo(numero_expediente)
    if resultado:
        st.success("Expediente encontrado:")
        st.json(resultado)  # Muestra el expediente en formato JSON
    else:
        st.error("No se encontro el expediente.")
        
# Aplicar estilos CSS para un fondo oscuro y un diseño similar a ChatGPT
st.markdown("""
    <style>
    /* Estilos generales */
    body {
        background-color: #1e1e1e;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #1e1e1e;
    }
    .css-1d391kg, .css-qrbaxs {
        background-color: #1e1e1e;
        color: white;
        font-size: 18px;
    }
    .css-10trblm {
        color: white;
    }
    /* Estilos para la barra lateral */
    .css-1lcbmhc {
        background-color: #252525 !important;
    }
    .css-1hynsf2 {
        font-size: 18px !important;
        font-weight: bold;
        color: #FFD700 !important; /* Amarillo dorado */
    }
    .css-16idsys {
        font-size: 16px !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Crear la barra lateral
st.sidebar.title("IA - Gestión de Expedientes")
menu = st.sidebar.radio("Navegación", ["Explorar Expedientes", "Chat", "Subir PDF"])

# Contenido de cada opciÃƒÂ³n
if menu == "Explorar Expedientes":
    st.title("Explorar Expedientes")
    st.write("Aquí podrás buscar y consultar expedientes almacenados en la base de datos.")

elif menu == "Chat":
    st.title("Chat con IA sobre Expedientes")
    st.write("Aquí podrás hacer preguntas sobre los expedientes y recibir respuestas.")

elif menu == "Subir PDF":
    st.title("Subir Documentos PDF")
    st.write("Aquí puedes cargar documentos para almacenarlos en la base de datos.")

# Mensaje de bienvenida
st.sidebar.markdown("---")
st.sidebar.markdown("*Proyecto en desarrollo por JKarlos2025IA*")
