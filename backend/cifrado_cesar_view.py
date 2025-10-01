import streamlit as st
from backend.criptografia import cifrado_cesar

def render():
    st.header("Cifrado César")
    st.markdown("""
    **Definición:** El cifrado César es una de las técnicas de cifrado más simples y conocidas. Es un tipo de cifrado por sustitución en el que cada letra en el texto original se reemplaza por una letra un número fijo de posiciones más adelante en el alfabeto.
    """)

    texto_original = st.text_area("Texto a procesar", "Hola Mundo!")
    desplazamiento = st.slider("Desplazamiento", 1, 25, 3)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cifrar"):
            if not texto_original:
                st.warning("Por favor, introduce un texto para cifrar.")
            else:
                texto_cifrado = cifrado_cesar(texto_original, desplazamiento, 'cifrar')
                st.success("Texto Cifrado:")
                st.code(texto_cifrado, language=None)

    with col2:
        if st.button("Descifrar"):
            if not texto_original:
                st.warning("Por favor, introduce un texto para descifrar.")
            else:
                texto_descifrado = cifrado_cesar(texto_original, desplazamiento, 'descifrar')
                st.info("Texto Descifrado:")
                st.code(texto_descifrado, language=None)