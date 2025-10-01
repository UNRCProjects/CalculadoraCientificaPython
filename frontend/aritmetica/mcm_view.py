import streamlit as st
from backend.aritmetica import mcm

def render():
    st.header("Mínimo Común Múltiplo (MCM)")
    st.markdown("""
    **Definición:** El Mínimo Común Múltiplo (MCM) de dos números es el menor número entero positivo que es múltiplo de ambos. Si uno de los números es 0, el MCM es 0 por convención.
    """)
    a = st.number_input("Número A", value=0, step=1)
    b = st.number_input("Número B", value=0, step=1)
    if st.button("Calcular MCM"):
        if a < 1 or b < 1:
            st.warning("Ambos números deben ser mayores o iguales a 1 para calcular el MCM.")
        else:
            st.success(f"MCM({a}, {b}) = {mcm(a, b)}")
