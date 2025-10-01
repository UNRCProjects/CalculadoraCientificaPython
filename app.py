from numpy import False_
import streamlit as st
from frontend.aritmetica import suma_view, division_view, aritmetica_view
from frontend.etl_view import render as etl_render
from frontend import home_view
from frontend import autores_view

# Configuración inicial de la app
st.set_page_config(
    page_title="Calculadora Colaborativa", 
    layout="wide"
)

# Inicializar session_state si no existe
if 'categoria' not in st.session_state:
    st.session_state['categoria'] = 'Home'
if 'subopcion' not in st.session_state:
    st.session_state['subopcion'] = 'Principal'

# ====== BARRA LATERAL ======
# st.sidebar.title("📂 Navegación")
st.sidebar.image("assets/logo_unrc.png")

# Sidebar con categorías y subopciones tipo dropdown
with st.sidebar.expander("🏠 Home", expanded=False):
    if st.button("Ir a Home", key="home_btn"):
        st.session_state['categoria'] = "Home"
        st.session_state['subopcion'] = "Principal"
    if st.button("Autores", key="autores_btn"):
        st.session_state['categoria'] = "Autores"


with st.sidebar.expander("🧮 Aritmética", expanded=False):
    if st.button("Suma", key="suma_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "Suma"
    if st.button("División", key="division_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "División"

with st.sidebar.expander("🧹 ETL (CSV)", expanded=False):
    if st.button("Procesar CSV", key="etl_btn"):
        st.session_state['categoria'] = "ETL"
        st.session_state['subopcion'] = "Procesar CSV"

# Ruteo según selección
categoria = st.session_state['categoria']
subopcion = st.session_state['subopcion']

if categoria == "Home":
    home_view.render()
elif categoria == "Aritmética" and subopcion == "Suma":
    suma_view.render()
elif categoria == "Aritmética" and subopcion == "División":
    division_view.render()
elif categoria == "Autores":
    autores_view.render()
elif categoria == "ETL" and subopcion == "Procesar CSV":
    etl_render()

# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)
