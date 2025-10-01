import streamlit as st
from backend.aritmetica import coprimos

def render():
    st.header("¿Dos números son coprimos?")
    st.markdown("""
    **Definición:** Dos números son coprimos (o primos entre sí) si su único divisor común es el 1, es decir, su MCD es 1.
    """)
    a = st.number_input("Número A", value=0, step=1, key="coprimo_a")
    b = st.number_input("Número B", value=0, step=1, key="coprimo_b")
    if st.button("Verificar coprimos"):
        if a < 1 or b < 1:
            st.warning("Ambos números deben ser mayores o iguales a 1 para analizar coprimalidad.")
        elif coprimos(a, b):
            st.success(f"{a} y {b} son coprimos (primos entre sí).")
        else:
            st.error(f"{a} y {b} NO son coprimos.")
