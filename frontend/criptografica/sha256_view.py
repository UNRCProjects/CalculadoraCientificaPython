import streamlit as st
from backend.criptografia import sha256_hash

def render():
    st.title("🔐 Hash SHA256")
    
    st.markdown("""
    ### Descripción
    SHA-256 es una función criptográfica hash diseñada por la Agencia de Seguridad Nacional 
    de los Estados Unidos. Produce un valor hash de 256 bits (32 bytes) para cualquier entrada.
    """)

    mensaje = st.text_area("Ingrese el texto a hashear", "Hello, World!")
    
    if st.button("Generar Hash"):
        try:
            hash_result = sha256_hash(mensaje)
            st.success("Hash generado exitosamente")
            st.code(hash_result)
            st.info(f"Longitud del hash: {len(hash_result)} caracteres")
        except Exception as e:
            st.error(f"Error: {str(e)}")