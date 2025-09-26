import streamlit as st
from backend.matrices import matriz_inversa, determinante

def render():
    st.header("Matriz Inversa")
    st.markdown("""
    **Definición:** La matriz inversa A⁻¹ de una matriz cuadrada A es tal que A × A⁻¹ = I (matriz identidad).
    Solo las matrices no singulares (determinante ≠ 0) tienen inversa.
    """)
    
    st.subheader("Matriz Cuadrada")
    tamaño = st.number_input("Tamaño de la matriz (n×n)", min_value=2, max_value=4, value=3, key="tamaño_inv")
    
    st.write(f"Ingrese los valores de la matriz {tamaño}×{tamaño} (separados por comas, filas separadas por punto y coma):")
    valores_text = st.text_input("Valores de la matriz", value="2,1,1;1,2,1;1,1,2", key="valores_inv")
    
    if st.button("Calcular Matriz Inversa"):
        try:
            # Parsear valores
            filas_list = valores_text.split(';')
            valores = []
            for fila in filas_list:
                valores_fila = [float(x.strip()) for x in fila.split(',')]
                valores.append(valores_fila)
            
            # Verificar si tiene inversa
            det = determinante(valores)
            if abs(det) < 1e-10:
                st.error("La matriz es singular (determinante = 0), no tiene inversa")
                return
            
            inversa = matriz_inversa(valores)
            
            st.success("Matriz inversa calculada exitosamente!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Matriz Original:**")
                st.write(valores)
                st.write(f"**Determinante:** {det:.6f}")
            with col2:
                st.write("**Matriz Inversa:**")
                st.write(inversa)
                
        except ValueError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Error inesperado: {e}")
