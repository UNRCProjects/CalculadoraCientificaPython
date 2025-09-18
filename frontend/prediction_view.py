# Importamos las herramientas que necesitamos de la librería scikit-learn.
import streamlit as st
import pandas as pd
from backend import prediction

def render():
    # Título de la página.
    st.title("📈 Módulo de Predicciones (Regresión Lineal)")

    # Primero, revisamos si se cargó un archivo en el módulo ETL.
    # Si no hay datos en st.session_state, mostramos una advertencia.
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Por favor, carga un archivo CSV en el módulo 'ETL y Análisis de Datos' primero.")
        return

    # Si hay datos, los cargamos y mostramos una vista previa.
    df = st.session_state.df
    st.info("Se utilizarán los datos cargados en el módulo ETL.")
    st.dataframe(df.head())

    st.markdown("### Configuración del Modelo")
    
    # Para un modelo de regresión, solo podemos usar columnas con números.
    # Aquí filtramos el DataFrame para quedarnos solo con esas.
    columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    # Verificamos que haya al menos dos columnas numéricas para poder hacer la regresión.
    if len(columnas_numericas) < 2:
        st.error("El conjunto de datos debe tener al menos dos columnas numéricas para la regresión.")
        return

    # Dividimos la sección en dos columnas para organizar los menús.
    col1, col2 = st.columns(2)
    with col1:
        # Creamos un menú para que el usuario elija qué columna quiere predecir (la variable 'Y').
        variable_objetivo = st.selectbox("Selecciona la variable a predecir (Y)", columnas_numericas)
    
    with col2:
        # Las características (variables 'X') son las columnas que usaremos para predecir.
        # No pueden incluir la variable que ya elegimos como objetivo.
        opciones_caracteristicas = [col for col in columnas_numericas if col != variable_objetivo]
        # st.multiselect permite al usuario elegir una o varias opciones de una lista.
        caracteristicas = st.multiselect("Selecciona las características (X)", opciones_caracteristicas, default=opciones_caracteristicas[0] if opciones_caracteristicas else [])

    # Cuando el usuario presiona el botón "Entrenar Modelo"...
    if st.button("Entrenar Modelo"):
        if not caracteristicas:
            st.error("Debes seleccionar al menos una característica.")
        else:
            # st.spinner muestra un mensaje de "cargando" mientras se ejecuta el código de adentro.
            with st.spinner("Entrenando el modelo..."):
                modelo, mse, r2 = prediction.entrenar_modelo_regresion(df, variable_objetivo, caracteristicas)
            
            st.success("¡Modelo entrenado exitosamente!")
            
            st.markdown("### Resultados del Modelo")
            # st.metric es una forma bonita de mostrar un número y su etiqueta.
            st.metric(label="Error Cuadrático Medio (MSE)", value=f"{mse:.2f}")
            st.metric(label="Coeficiente de Determinación (R²)", value=f"{r2:.2f}")
            
            st.info("El R² indica qué tan bien las características explican la variabilidad de la variable objetivo. Un valor cercano a 1 es mejor.")

