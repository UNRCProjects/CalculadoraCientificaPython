import streamlit as st
from frontend.aritmetica import suma_view, division_view, aritmetica_view
from frontend import home_view
from frontend import autores_view
# Importamos la nueva vista de visualización
from frontend.visualizacion import scatter_view

# Configuración inicial de la app
st.set_page_config(
    page_title="Calculadora Colaborativa", 
    layout="wide"
)

# --- Definición de las Vistas y Navegación ---
# Estructura para registrar todas las vistas disponibles en la aplicación.
PAGES = {
    "Home": {
        "Principal": home_view.render,
        "Autores": autores_view.render,
    },
    "Aritmética": {
        "Suma": suma_view.render,
        "División": division_view.render,
    },
    "Visualización": {
        "Gráfico de Dispersión": scatter_view.render,
    }
}

# ====== BARRA LATERAL ======
st.sidebar.image("assets/logo_unrc.png")

# Selección de categoría principal
st.sidebar.title("📂 Navegación")
categoria_seleccionada = st.sidebar.radio("Módulo", list(PAGES.keys()))

# Selección de subopción dentro de la categoría
subopciones = PAGES[categoria_seleccionada]
subopcion_seleccionada = st.sidebar.radio("Operación", list(subopciones.keys()))

# --- Renderizado de la Vista ---
# Se busca la función correspondiente en el diccionario y se ejecuta.
render_function = PAGES[categoria_seleccionada][subopcion_seleccionada]
render_function()


# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)
