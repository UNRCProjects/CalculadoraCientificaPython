import streamlit as st
from backend.criptografia import generate_rsa_keys, rsa_encrypt, rsa_decrypt

def render():
    st.title("🔐 Cifrado RSA")
    
    st.markdown("""
    ### Descripción
    RSA es un sistema criptográfico de clave pública desarrollado por Rivest, Shamir y Adleman.
    Es uno de los primeros sistemas prácticos de cifrado de clave pública y se usa ampliamente 
    para la transmisión segura de datos.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        p = st.number_input("Ingrese el primer número primo (p)", min_value=2, value=61)
        q = st.number_input("Ingrese el segundo número primo (q)", min_value=2, value=53)
        mensaje = st.text_input("Mensaje a cifrar", "HELLO")

    if st.button("Generar claves y cifrar"):
        try:
            public_key, private_key = generate_rsa_keys(p, q)
            encrypted = rsa_encrypt(mensaje, public_key)
            decrypted = rsa_decrypt(encrypted, private_key)
            
            with col2:
                st.success("Claves generadas exitosamente")
                st.write("Clave pública:", public_key)
                st.write("Clave privada:", private_key)
                st.write("Mensaje cifrado:", encrypted)
                st.write("Mensaje descifrado:", decrypted)
        except Exception as e:
            st.error(f"Error: {str(e)}")