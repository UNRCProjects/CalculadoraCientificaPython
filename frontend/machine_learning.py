import streamlit as st
import pandas as pd
from backend.machine_learning import entrenar_modelo_clasificacion


def render():
    st.title("Módulo de Machine Learning")
    st.write("Sube un archivo CSV para aplicar un modelo de clasificación básico.")

    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Vista previa de los datos:")
        st.dataframe(df.head())

        columnas = df.columns.tolist()
        target_col = st.selectbox("Selecciona la columna objetivo (variable a predecir):", columnas)
        feature_cols = st.multiselect("Selecciona las columnas de entrada (features):", [col for col in columnas if col != target_col], default=[col for col in columnas if col != target_col])

        if st.button("Entrenar modelo de clasificación"):  # Botón para ejecutar ML
            if not feature_cols or not target_col:
                st.warning("Debes seleccionar al menos una columna de entrada y una columna objetivo.")
            else:
                st.write("Entrenando modelo...")
                acc, reporte = entrenar_modelo_clasificacion(df, feature_cols, target_col)
                st.success(f"Precisión del modelo: {acc:.2f}")
                st.text("Reporte de clasificación:")
                st.text(reporte)
