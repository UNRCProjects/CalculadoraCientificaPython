import streamlit as st
from frontend.aritmetica import mcd_view, mcm_view, primos_view, coprimos_view
from frontend.series_temporales import (
    generar_datos_render, 
    analizar_estacionariedad_render, 
    entrenar_modelo_render, 
    predicciones_render, 
    metricas_render
)
from frontend import home_view
from frontend import autores_view

# Configuración inicial de la app
st.set_page_config(
    page_title="Calculadora Colaborativa",
    page_icon="assets/favicon.ico",
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

with st.sidebar.expander("🧮 Aritmética"):
    if st.button("Máximo Común Divisor (MCD)", key="mcd_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "MCD"
    if st.button("Mínimo Común Multiplo (MCM)", key="mcm_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "MCM"
    if st.button("Número primo", key="primos_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "Primos"
    if st.button("Números coprimos", key="coprimos_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "Coprimos"

with st.sidebar.expander("📈 Series Temporales"):
    if st.button("Generar Datos", key="generar_datos_btn"):
        st.session_state['categoria'] = "Series Temporales"
        st.session_state['subopcion'] = "Generar Datos"
    if st.button("Análisis Estacionariedad", key="estacionariedad_btn"):
        st.session_state['categoria'] = "Series Temporales"
        st.session_state['subopcion'] = "Estacionariedad"
    if st.button("Entrenar Modelo", key="entrenar_btn"):
        st.session_state['categoria'] = "Series Temporales"
        st.session_state['subopcion'] = "Entrenar Modelo"
    if st.button("Predicciones", key="predicciones_btn"):
        st.session_state['categoria'] = "Series Temporales"
        st.session_state['subopcion'] = "Predicciones"
    if st.button("Métricas", key="metricas_btn"):
        st.session_state['categoria'] = "Series Temporales"
        st.session_state['subopcion'] = "Métricas"


# Ruteo según selección
categoria = st.session_state['categoria']
subopcion = st.session_state['subopcion']

if categoria == "Home":
    home_view.render()
elif categoria == "Aritmética" and subopcion == "MCD":
    mcd_view.render()
elif categoria == "Aritmética" and subopcion == "MCM":
    mcm_view.render()
elif categoria == "Aritmética" and subopcion == "Primos":
    primos_view.render()
elif categoria == "Aritmética" and subopcion == "Coprimos":
    coprimos_view.render()
elif categoria == "Series Temporales" and subopcion == "Generar Datos":
    generar_datos_render()
elif categoria == "Series Temporales" and subopcion == "Estacionariedad":
    analizar_estacionariedad_render()
elif categoria == "Series Temporales" and subopcion == "Entrenar Modelo":
    entrenar_modelo_render()
elif categoria == "Series Temporales" and subopcion == "Predicciones":
    predicciones_render()
elif categoria == "Series Temporales" and subopcion == "Métricas":
    metricas_render()
elif categoria == "Autores":
    autores_view.render()

# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)

