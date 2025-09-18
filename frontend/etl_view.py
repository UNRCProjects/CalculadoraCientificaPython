# Importamos las librerías necesarias.
import streamlit as st
from backend import etl
import io

def render():
    # Título de la página.
    st.title("🔄 Módulo de ETL y Análisis de Datos")

    st.markdown("Sube un archivo en formato CSV para realizar un análisis exploratorio de los datos (EDA).")

    # Creamos el widget para que el usuario suba su archivo.
    archivo_subido = st.file_uploader("Elige un archivo CSV", type=['csv'])

    # Si el usuario sube un archivo...
    if archivo_subido is not None:
        # Llamamos a la función del backend para cargar los datos.
        # El resultado se guarda en el estado de la sesión para que otros módulos puedan usarlo.
        st.session_state.df = etl.cargar_datos(archivo_subido)

    # Si ya hay un DataFrame cargado en la sesión, mostramos el análisis.
    if 'df' in st.session_state and st.session_state.df is not None:
        st.success("¡Archivo cargado y procesado exitosamente!")
        df = st.session_state.df

        st.markdown("### Vista Previa de los Datos")
        st.dataframe(df.head())

        st.markdown("### Análisis Exploratorio Básico")
        
        # Usamos 'expanders' para organizar la información y no saturar la pantalla.
        with st.expander("Información General del DataFrame"):
            st.write("Dimensiones:", df.shape)
            # Capturamos la salida de df.info() para mostrarla de forma limpia.
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())

        with st.expander("Estadísticas Descriptivas (para columnas numéricas)"):
            st.write(df.describe())

        with st.expander("Conteo de Valores Faltantes (Nulos) por Columna"):
            st.write(df.isnull().sum())

        # --- Nueva sección para Limpieza de Datos ---
        st.markdown("### Limpieza y Preprocesamiento de Datos")
        with st.expander("Manejo de Valores Faltantes (NaN)"):
            st.markdown("Los modelos de Machine Learning no pueden trabajar con datos faltantes. Elige una estrategia para manejarlos.")
            
            # Creamos una copia del dataframe original para no alterarlo en la sesión hasta que se aplique la limpieza
            df_limpio = df.copy()

            opcion_limpieza = st.selectbox(
                "Estrategia de limpieza:",
                ["No hacer nada", "Eliminar filas con valores faltantes", "Rellenar con la media (solo columnas numéricas)"]
            )

            if st.button("Aplicar Limpieza"):
                if opcion_limpieza == "Eliminar filas con valores faltantes":
                    df_limpio.dropna(inplace=True)
                    st.session_state.df = df_limpio
                    st.success(f"Se eliminaron las filas con valores nulos. Nuevo tamaño del DataFrame: {df_limpio.shape}")
                    st.rerun() # Recargamos la app para que todos los módulos vean el cambio
                
                elif opcion_limpieza == "Rellenar con la media (solo columnas numéricas)":
                    for col in df_limpio.select_dtypes(include=['float64', 'int64']).columns:
                        df_limpio[col].fillna(df_limpio[col].mean(), inplace=True)
                    st.session_state.df = df_limpio
                    st.success("Se rellenaron los valores nulos en columnas numéricas con su media.")
                    st.rerun() # Recargamos la app

    else:
        # Si no hay archivo cargado, mostramos una advertencia.
        st.info("Esperando la carga de un archivo CSV para comenzar.")