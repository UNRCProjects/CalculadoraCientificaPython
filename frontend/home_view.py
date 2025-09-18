# Importamos streamlit para poder crear los elementos de la página.
import streamlit as st

def render():
    # st.title() crea el título más grande de la página.
    st.title("Calculadora de Ciencia de Datos")
    
    # st.subheader() crea un subtítulo.
    st.subheader("Bienvenido 👋")
    
    # st.write() nos permite escribir texto normal o con formato Markdown.
    # Las tres comillas dobles nos dejan escribir en varias líneas.
    st.write("""
    Esta calculadora es un proyecto que integra múltiples módulos de 
    matemáticas, estadística, ciencia de datos e inteligencia artificial.  

    Puedes navegar entre los distintos módulos desde el menú lateral (a la izquierda).  
    Cada módulo incluye **operaciones específicas** con su propia interfaz.
    """)
    
    # st.markdown() es para escribir texto con formato (como negritas, listas, etc.).
    st.markdown("### 📚 Módulos disponibles")
    st.markdown("""
    - 🧮 **Aritmética**: Operaciones matemáticas básicas.
    - 🔄 **ETL y Análisis de Datos**: Carga y explora tus propios conjuntos de datos.
    - 📈 **Predicciones (Machine Learning)**: Entrena modelos de regresión sencillos.
    """)
    
    # st.info() muestra un cuadro de información de color azul.
    st.info("👉 Selecciona un módulo en el menú lateral para comenzar.")
