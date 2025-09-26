import streamlit as st
from backend.matrices import determinante

def render():
    st.header("Determinante de Matriz")
    st.markdown("""
    **Definición:** El determinante es un valor escalar que se puede calcular solo para matrices cuadradas.
    Es útil para determinar si una matriz tiene inversa y para resolver sistemas de ecuaciones lineales.
    """)
    
    st.subheader("Matriz Cuadrada")
    tamaño = st.number_input("Tamaño de la matriz (n×n)", min_value=2, max_value=4, value=3, key="tamaño_det")
    
    st.write(f"Ingrese los valores de la matriz {tamaño}×{tamaño} (separados por comas, filas separadas por punto y coma):")
    valores_text = st.text_input("Valores de la matriz", value="1,2,3;4,5,6;7,8,9", key="valores_det")
    
    if st.button("Calcular Determinante"):
        try:
            # Parsear valores
            filas_list = valores_text.split(';')
            valores = []
            for fila in filas_list:
                valores_fila = [float(x.strip()) for x in fila.split(',')]
                valores.append(valores_fila)
            
            det = determinante(valores)
            
            st.success("Determinante calculado exitosamente!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Matriz:**")
                st.write(valores)
            with col2:
                st.write("**Determinante:**")
                st.write(f"det(A) = {det:.6f}")
                
            if abs(det) < 1e-10:
                st.warning("⚠️ El determinante es muy cercano a cero. La matriz puede ser singular.")
            else:
                st.info("✅ La matriz es no singular y tiene inversa.")
                
        except ValueError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Error inesperado: {e}")
