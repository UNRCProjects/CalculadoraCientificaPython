import streamlit as st
import numpy as np
import math
from backend.criptografia import hill_encrypt, hill_decrypt

def show():
    st.title("Hill Cipher")
    
    st.markdown("""
    The Hill cipher is a polygraphic substitution cipher based on linear algebra.
    It uses a matrix as the key to encrypt blocks of letters in the plaintext.
    This implementation uses a 2x2 matrix for encryption and decryption.
    """)
    
    # Matrix input
    st.subheader("Key Matrix (2x2)")
    col1, col2 = st.columns(2)
    
    with col1:
        a11 = st.number_input("Enter a11", value=2, key="a11")
        a21 = st.number_input("Enter a21", value=3, key="a21")
    
    with col2:
        a12 = st.number_input("Enter a12", value=1, key="a12")
        a22 = st.number_input("Enter a22", value=4, key="a22")
    
    # Create key matrix
    key_matrix = np.array([[a11, a12], [a21, a22]])
    
    # Message input
    message = st.text_input("Enter your message (letters only)", "HELLO")
    
    # Check if matrix is valid
    try:
        det = int(np.round(np.linalg.det(key_matrix)))
        if det == 0 or math.gcd(det % 26, 26) != 1:
            st.error("Invalid key matrix. The determinant must be non-zero and coprime with 26.")
            return
    except Exception as e:
        st.error(f"Error with key matrix: {str(e)}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Encrypt"):
            if message:
                try:
                    encrypted = hill_encrypt(message, key_matrix)
                    st.success("Message encrypted!")
                    st.write("Original text:", message)
                    st.write("Encrypted text:", encrypted)
                except Exception as e:
                    st.error(f"Encryption error: {str(e)}")
    
    with col2:
        if st.button("Decrypt"):
            if message:
                try:
                    decrypted = hill_decrypt(message, key_matrix)
                    st.success("Message decrypted!")
                    st.write("Original text:", message)
                    st.write("Decrypted text:", decrypted)
                except Exception as e:
                    st.error(f"Decryption error: {str(e)}")
    
    # Educational section
    with st.expander("How it works"):
        st.markdown("""
        1. The message is divided into pairs of letters
        2. Each pair is converted to numbers (A=0, B=1, etc.)
        3. The numbers are multiplied by the key matrix
        4. The result is converted back to letters
        5. For decryption, the inverse of the key matrix is used
        
        Note: The key matrix must have a determinant that is non-zero and coprime with 26.
        """)