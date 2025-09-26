import streamlit as st
from backend.matrices import multiplicacion_matrices

def render():
    st.header("Multiplicación de Matrices")
    st.markdown("""
    **Definición:** La multiplicación de matrices A (m×n) y B (n×p) resulta en una matriz C (m×p) 
    donde c_ij = Σ(a_ik * b_kj) para k de 1 a n.
    """)
    
    st.subheader("Matriz A")
    col1, col2 = st.columns(2)
    with col1:
        filas_a = st.number_input("Filas de A", min_value=1, max_value=5, value=2, key="filas_a_mult")
    with col2:
        columnas_a = st.number_input("Columnas de A", min_value=1, max_value=5, value=3, key="columnas_a_mult")
    
    st.write("Ingrese los valores de la matriz A (separados por comas, filas separadas por punto y coma):")
    valores_a_text = st.text_input("Valores de A", value="1,2,3;4,5,6", key="valores_a_mult")
    
    st.subheader("Matriz B")
    col1, col2 = st.columns(2)
    with col1:
        filas_b = st.number_input("Filas de B", min_value=1, max_value=5, value=3, key="filas_b_mult")
    with col2:
        columnas_b = st.number_input("Columnas de B", min_value=1, max_value=5, value=2, key="columnas_b_mult")
    
    st.write("Ingrese los valores de la matriz B (separados por comas, filas separadas por punto y coma):")
    valores_b_text = st.text_input("Valores de B", value="7,8;9,10;11,12", key="valores_b_mult")
    
    if st.button("Calcular Multiplicación"):
        try:
            # Parsear valores de A
            filas_a_list = valores_a_text.split(';')
            valores_a = []
            for fila in filas_a_list:
                valores_fila = [float(x.strip()) for x in fila.split(',')]
                valores_a.append(valores_fila)
            
            # Parsear valores de B
            filas_b_list = valores_b_text.split(';')
            valores_b = []
            for fila in filas_b_list:
                valores_fila = [float(x.strip()) for x in fila.split(',')]
                valores_b.append(valores_fila)
            
            resultado = multiplicacion_matrices(valores_a, valores_b)
            
            st.success("Multiplicación calculada exitosamente!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Matriz A:**")
                st.write(valores_a)
            with col2:
                st.write("**Matriz B:**")
                st.write(valores_b)
            with col3:
                st.write("**Resultado A × B:**")
                st.write(resultado)
                
        except ValueError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Error inesperado: {e}")
