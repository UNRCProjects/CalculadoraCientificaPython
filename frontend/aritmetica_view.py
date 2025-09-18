# Importamos streamlit para la interfaz y nuestro backend de aritmetica para las operaciones.
import streamlit as st
from backend import aritmetica

def render():
    # Título de la página del módulo.
    st.title("🧮 Módulo de Aritmética")

    # Creamos un menú desplegable para que el usuario elija la operación.
    operacion = st.selectbox("Selecciona una operación", 
                             ["Suma", "Resta", "Multiplicación", "División", "Raíz Cuadrada"])

    st.markdown("---")

    # Si la operación necesita dos números (como suma, resta, etc.).
    if operacion in ["Suma", "Resta", "Multiplicación", "División"]:
        # st.columns(2) divide el espacio en dos columnas para poner los inputs uno al lado del otro.
        col1, col2 = st.columns(2)
        with col1:
            # st.number_input() crea un campo para que el usuario ingrese un número.
            num1 = st.number_input("Primer número", value=0.0, format="%.2f")
        with col2:
            num2 = st.number_input("Segundo número", value=0.0, format="%.2f")

        # st.button() crea un botón. El código dentro del 'if' solo se ejecuta si se hace clic.
        if st.button("Calcular"):
            resultado = 0
            # Dependiendo de la operación elegida, llamamos a la función correspondiente del backend.
            if operacion == "Suma":
                resultado = aritmetica.sumar(num1, num2)
            elif operacion == "Resta":
                resultado = aritmetica.restar(num1, num2)
            elif operacion == "Multiplicación":
                resultado = aritmetica.multiplicar(num1, num2)
            elif operacion == "División":
                resultado = aritmetica.dividir(num1, num2)
            
            # st.success() muestra un mensaje de éxito de color verde con el resultado.
            st.success(f"El resultado de la {operacion.lower()} es: **{resultado}**")

    # Si la operación es Raíz Cuadrada, solo necesitamos un número.
    elif operacion == "Raíz Cuadrada":
        num = st.number_input("Ingresa el número", value=0.0, format="%.2f")
        if st.button("Calcular"):
            resultado = aritmetica.raiz_cuadrada(num)
            st.success(f"El resultado es: **{resultado}**")
