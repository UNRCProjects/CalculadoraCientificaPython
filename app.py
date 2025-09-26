import streamlit as st
from frontend.aritmetica import mcd_view, mcm_view, primos_view, coprimos_view
from frontend.matrices import suma_render, multiplicacion_render, determinante_render, inversa_render
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

with st.sidebar.expander("🔢 Álgebra Lineal"):
    if st.button("Suma de Matrices", key="suma_matrices_btn"):
        st.session_state['categoria'] = "Álgebra Lineal"
        st.session_state['subopcion'] = "Suma"
    if st.button("Multiplicación de Matrices", key="mult_matrices_btn"):
        st.session_state['categoria'] = "Álgebra Lineal"
        st.session_state['subopcion'] = "Multiplicacion"
    if st.button("Determinante", key="det_matrices_btn"):
        st.session_state['categoria'] = "Álgebra Lineal"
        st.session_state['subopcion'] = "Determinante"
    if st.button("Matriz Inversa", key="inv_matrices_btn"):
        st.session_state['categoria'] = "Álgebra Lineal"
        st.session_state['subopcion'] = "Inversa"

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
elif categoria == "Álgebra Lineal" and subopcion == "Suma":
    suma_render()
elif categoria == "Álgebra Lineal" and subopcion == "Multiplicacion":
    multiplicacion_render()
elif categoria == "Álgebra Lineal" and subopcion == "Determinante":
    determinante_render()
elif categoria == "Álgebra Lineal" and subopcion == "Inversa":
    inversa_render()

# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)
