import streamlit as st
from backend.criptografia import caesar_encrypt, caesar_decrypt

def render():
    st.title("📜 Cifrado Caesar")
    
    st.markdown("""
    ### Descripción
    El cifrado César es una de las técnicas de cifrado más simples y conocidas. 
    Es un tipo de cifrado por sustitución en el que cada letra del texto plano 
    se reemplaza por una letra que se encuentra un número fijo de posiciones 
    más adelante en el alfabeto.
    """)

    mensaje = st.text_input("Mensaje", "HELLO")
    desplazamiento = st.slider("Desplazamiento", 1, 25, 3)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Cifrar"):
            try:
                resultado = caesar_encrypt(mensaje, desplazamiento)
                st.success("Mensaje cifrado:")
                st.code(resultado)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("Descifrar"):
            try:
                resultado = caesar_decrypt(mensaje, desplazamiento)
                st.success("Mensaje descifrado:")
                st.code(resultado)
            except Exception as e:
                st.error(f"Error: {str(e)}")