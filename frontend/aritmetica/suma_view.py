import streamlit as st
from backend.aritmetica import suma

def render():
    st.header("Suma de dos números")
    a = st.number_input("Ingrese el primer número", value=0)
    b = st.number_input("Ingrese el segundo número", value=0)
    if st.button("Sumar"):
        resultado = suma(a, b)
        st.success(f"El resultado de la suma es: {resultado}")
