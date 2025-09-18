# Importamos pandas para poder trabajar con los datos como si fueran tablas de Excel (DataFrames).
import pandas as pd
# Importamos streamlit para poder mostrar errores en la página si algo sale mal.
import streamlit as st

# El decorador @st.cache_data es un truco de Streamlit para que no tenga que recargar el archivo
# cada vez que hacemos un cambio en la página. Así la app es más rápida.
@st.cache_data
def cargar_datos(archivo_subido):
    # Esta función recibe el archivo que el usuario subió.
    if archivo_subido is not None:
        try:
            # Intentamos leer el archivo CSV con pandas y lo convertimos en un DataFrame.
            df = pd.read_csv(archivo_subido)
            return df
        except Exception as e:
            # Si hay algún problema al leer el archivo, mostramos un error en la página.
            st.error(f"Error al leer el archivo: {e}")
    return None