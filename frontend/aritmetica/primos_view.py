import streamlit as st
from backend.aritmetica import es_primo

def render():
    st.header("¿Un número es primo?")
    st.markdown("""
    **Definición:** Un número primo es aquel que solo es divisible por 1 y por sí mismo. El primer número primo es el 2.
    """)
    n = st.number_input("Número a verificar", value=0, step=1)
    if st.button("Verificar primo"):
        if n < 2:
            st.warning("Por definición, los números menores a 2 no son primos.")
        elif es_primo(n):
            st.success(f"{n} es un número primo.")
        else:
            st.error(f"{n} NO es un número primo.")
