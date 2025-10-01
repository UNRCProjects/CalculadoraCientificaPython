import streamlit as st
from backend.criptografia import caesar_encrypt, caesar_decrypt

def show():
    st.title("Caesar Cipher")
    
    st.markdown("""
    The Caesar Cipher is one of the simplest and most widely known encryption techniques.
    It is a type of substitution cipher in which each letter in the plaintext is shifted a certain number of places down the alphabet.
    """)
    
    # Input section
    message = st.text_input("Enter your message", "HELLO")
    shift = st.number_input("Enter shift value (1-25)", min_value=1, max_value=25, value=3)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Encrypt"):
            if message:
                encrypted = caesar_encrypt(message, shift)
                st.success("Message encrypted!")
                st.write("Original text:", message)
                st.write("Encrypted text:", encrypted)
            else:
                st.error("Please enter a message to encrypt.")
    
    with col2:
        if st.button("Decrypt"):
            if message:
                decrypted = caesar_decrypt(message, shift)
                st.success("Message decrypted!")
                st.write("Original text:", message)
                st.write("Decrypted text:", decrypted)
            else:
                st.error("Please enter a message to decrypt.")
    
    # Educational section
    with st.expander("How it works"):
        st.markdown("""
        1. Each letter in the message is shifted down the alphabet by the shift value
        2. For example, with a shift of 3:
           - A → D
           - B → E
           - C → F
           And so on...
        3. The shift wraps around the alphabet (Z with shift 3 becomes C)
        4. Numbers and special characters remain unchanged
        """)