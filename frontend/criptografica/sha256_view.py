import streamlit as st
from backend.criptografia import sha256_hash

def show():
    st.title("SHA256 Hash Generator")
    
    st.markdown("""
    SHA-256 (Secure Hash Algorithm 256-bit) is a cryptographic hash function that generates a fixed-size 256-bit (32-byte) hash.
    It's commonly used for digital signatures and blockchain technology.
    """)
    
    # Input text
    message = st.text_area("Enter text to hash", "Hello, World!")
    
    if st.button("Generate Hash"):
        if message:
            # Generate hash
            hash_value = sha256_hash(message)
            
            # Display results
            st.success("Hash generated successfully!")
            st.write("Original Text:", message)
            st.code(hash_value, language=None)
            
            # Additional information
            st.info(f"""
            Hash length: {len(hash_value)} characters
            This is a one-way function - you cannot decrypt a SHA256 hash back to the original text.
            """)
        else:
            st.error("Please enter some text to hash.")