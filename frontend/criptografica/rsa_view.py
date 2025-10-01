import streamlit as st
from backend.criptografia import generate_rsa_keys, rsa_encrypt, rsa_decrypt

def show():
    st.title("RSA Encryption/Decryption")
    
    st.markdown("""
    RSA (Rivest-Shamir-Adleman) is a public-key cryptosystem that is widely used for secure data transmission.
    Enter two prime numbers and your message to see RSA encryption in action.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        p = st.number_input("Enter first prime number (p)", min_value=2, value=61)
        q = st.number_input("Enter second prime number (q)", min_value=2, value=53)
    
    message = st.text_input("Enter message to encrypt", "HELLO")
    
    if st.button("Encrypt/Decrypt"):
        try:
            # Generate keys
            public_key, private_key = generate_rsa_keys(p, q)
            
            # Encrypt
            encrypted_msg = rsa_encrypt(message, public_key)
            
            # Decrypt
            decrypted_msg = rsa_decrypt(encrypted_msg, private_key)
            
            # Display results
            st.success("Encryption/Decryption successful!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("Public Key (e, n):", public_key)
                st.write("Private Key (d, n):", private_key)
            
            st.write("Original Message:", message)
            st.write("Encrypted (numeric form):", encrypted_msg)
            st.write("Decrypted Message:", decrypted_msg)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Make sure both numbers are prime and the message contains valid characters.")