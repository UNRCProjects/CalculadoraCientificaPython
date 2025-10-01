import streamlit as st
from backend.aritmetica import mcd

def render():
    st.header("Máximo Común Divisor (MCD)")
    st.markdown("""
    **Definición:** El Máximo Común Divisor (MCD) de dos números es el número más grande que los divide a ambos sin dejar residuo. Si el MCD es 1, los números son coprimos.
    """)
    a = st.number_input("Número A", value=0, step=1)
    b = st.number_input("Número B", value=0, step=1)
    if st.button("Calcular MCD"):
        if a < 1 or b < 1:
            st.warning("Ambos números deben ser mayores o iguales a 1 para calcular el MCD.")
        else:
            st.success(f"MCD({a}, {b}) = {mcd(a, b)}")
