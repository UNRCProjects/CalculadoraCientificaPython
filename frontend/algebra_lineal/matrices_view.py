import streamlit as st
from backend.algebra_lineal import multiplicar_matrices

def render():
    st.header("Multiplicación de Matrices")
    st.markdown("""
    **Definición:** La multiplicación de matrices es una operación binaria que produce una matriz a partir de dos matrices. 
    Para que la multiplicación sea posible, el número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.
    """)
    
    # Inputs simples para matrices 2x2
    st.subheader("Matriz A (2x2)")
    a11 = st.number_input("A[1,1]", value=0, key="a11")
    a12 = st.number_input("A[1,2]", value=0, key="a12")
    a21 = st.number_input("A[2,1]", value=0, key="a21")
    a22 = st.number_input("A[2,2]", value=0, key="a22")
    
    st.subheader("Matriz B (2x2)")
    b11 = st.number_input("B[1,1]", value=0, key="b11")
    b12 = st.number_input("B[1,2]", value=0, key="b12")
    b21 = st.number_input("B[2,1]", value=0, key="b21")
    b22 = st.number_input("B[2,2]", value=0, key="b22")
    
    if st.button("Calcular Multiplicación"):
        try:
            matriz_a = [[a11, a12], [a21, a22]]
            matriz_b = [[b11, b12], [b21, b22]]
            
            resultado = multiplicar_matrices(matriz_a, matriz_b)
            
            # Mostrar resultado de forma simple
            st.success(f"Resultado: A × B = [[{resultado[0][0]}, {resultado[0][1]}], [{resultado[1][0]}, {resultado[1][1]}]]")
            
        except Exception as e:
            st.error(f"Error al calcular la multiplicación: {str(e)}")
