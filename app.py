# Importamos streamlit, que es la librería para crear la página web.
import streamlit as st

# --- Solución al problema de importación ---
# Añadimos la ruta raíz del proyecto al sys.path de Python.
# Esto asegura que los módulos en 'frontend' y 'backend' se puedan importar sin problemas.
import sys
sys.path.append('.')
# Importamos las "vistas" de cada módulo. Cada vista es una parte de nuestra página.
from frontend import home_view, aritmetica_view, etl_view, prediction_view

# --- Configuración de la Página ---
# Esto es para que la pestaña del navegador tenga un título y un ícono.
st.set_page_config(
    page_title="Calculadora de Ciencia de Datos",
    page_icon="🔬", # Un emoji para el ícono.
    layout="wide"
)

# --- Menú de Navegación en la Barra Lateral ---
st.sidebar.title("📚 Módulos")

# Creamos un diccionario para guardar nuestras páginas. La clave es el nombre que se ve en el menú.
PAGES = {
    "Inicio": home_view,
    "🧮 Aritmética": aritmetica_view,
    "🔄 ETL y Análisis de Datos": etl_view,
    "📈 Predicciones (Machine Learning)": prediction_view
}

# Creamos el menú de radio botones en la barra lateral.
selection = st.sidebar.radio("Ir a", list(PAGES.keys()))

# Dependiendo de lo que el usuario elija, cargamos la página correspondiente.
page = PAGES[selection]
page.render() # Esta línea "dibuja" la página que elegimos.

st.sidebar.info("Proyecto desarrollado para la práctica de Ciencia de Datos.")
