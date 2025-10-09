import streamlit as st
import numpy as np
import pandas as pd

def render():
    st.header("🔢 Inversa de Matrices")
    
    st.markdown("""
    ### ¿Qué es la Inversa de una Matriz?
    
    La inversa de una matriz A es otra matriz A⁻¹ tal que:
    
    **A × A⁻¹ = A⁻¹ × A = I**
    
    Donde I es la matriz identidad. No todas las matrices tienen inversa.
    Una matriz tiene inversa si y solo si su determinante es diferente de cero.
    """)
    
    # Información sobre matrices invertibles
    st.markdown("""
    **Condiciones para que una matriz tenga inversa:**
    - ✅ La matriz debe ser cuadrada (mismo número de filas y columnas)
    - ✅ El determinante debe ser diferente de cero
    - ✅ La matriz debe ser no singular
    """)
    
    # Sección principal
    st.subheader("🧮 Calculadora de Inversa de Matrices")
    
    # Opciones de entrada
    opcion_entrada = st.radio(
        "Selecciona el método de entrada:",
        ["Matriz 2x2", "Matriz 3x3", "Matriz personalizada", "Matriz desde archivo"]
    )
    
    if opcion_entrada == "Matriz 2x2":
        render_matriz_2x2()
    elif opcion_entrada == "Matriz 3x3":
        render_matriz_3x3()
    elif opcion_entrada == "Matriz personalizada":
        render_matriz_personalizada()
    elif opcion_entrada == "Matriz desde archivo":
        render_matriz_archivo()
    
    # Información adicional
    st.subheader("ℹ️ Información Adicional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Propiedades de la Inversa:**
        - (A⁻¹)⁻¹ = A
        - (AB)⁻¹ = B⁻¹A⁻¹
        - (Aᵀ)⁻¹ = (A⁻¹)ᵀ
        - det(A⁻¹) = 1/det(A)
        """)
    
    with col2:
        st.markdown("""
        **Métodos de Cálculo:**
        - **Eliminación Gaussiana**
        - **Método de la adjunta**
        - **Descomposición LU**
        - **Método de Cholesky**
        """)

def render_matriz_2x2():
    """Renderiza la calculadora para matrices 2x2"""
    st.subheader("📐 Matriz 2x2")
    
    st.markdown("Ingresa los elementos de la matriz 2x2:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        a11 = st.number_input("a₁₁", value=1.0, key="a11_2x2")
        a21 = st.number_input("a₂₁", value=0.0, key="a21_2x2")
    
    with col2:
        a12 = st.number_input("a₁₂", value=0.0, key="a12_2x2")
        a22 = st.number_input("a₂₂", value=1.0, key="a22_2x2")
    
    # Crear matriz
    matriz = np.array([[a11, a12], [a21, a22]])
    
    # Mostrar matriz original
    st.write("**Matriz original:**")
    df_original = pd.DataFrame(matriz, index=['Fila 1', 'Fila 2'], columns=['Col 1', 'Col 2'])
    st.dataframe(df_original, use_container_width=True)
    
    # Calcular inversa
    if st.button("🔢 Calcular Inversa", key="calc_inv_2x2"):
        try:
            # Verificar si es invertible
            det = np.linalg.det(matriz)
            st.write(f"**Determinante:** {det:.6f}")
            
            if abs(det) < 1e-10:
                st.error("❌ La matriz no es invertible (determinante ≈ 0)")
            else:
                inversa = np.linalg.inv(matriz)
                
                st.success("✅ Matriz invertible")
                
                # Mostrar inversa
                st.write("**Matriz inversa:**")
                df_inversa = pd.DataFrame(inversa, index=['Fila 1', 'Fila 2'], columns=['Col 1', 'Col 2'])
                st.dataframe(df_inversa, use_container_width=True)
                
                # Verificar resultado
                identidad = np.dot(matriz, inversa)
                st.write("**Verificación (A × A⁻¹):**")
                df_verificacion = pd.DataFrame(identidad, index=['Fila 1', 'Fila 2'], columns=['Col 1', 'Col 2'])
                st.dataframe(df_verificacion, use_container_width=True)
                
                # Mostrar fórmula para matriz 2x2
                st.subheader("📝 Fórmula para Matriz 2x2")
                st.latex(r"""
                A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
                """)
                st.latex(r"""
                A^{-1} = \frac{1}{ad-bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix}
                """)
                
        except Exception as e:
            st.error(f"❌ Error al calcular la inversa: {str(e)}")

def render_matriz_3x3():
    """Renderiza la calculadora para matrices 3x3"""
    st.subheader("📐 Matriz 3x3")
    
    st.markdown("Ingresa los elementos de la matriz 3x3:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        a11 = st.number_input("a₁₁", value=1.0, key="a11_3x3")
        a21 = st.number_input("a₂₁", value=0.0, key="a21_3x3")
        a31 = st.number_input("a₃₁", value=0.0, key="a31_3x3")
    
    with col2:
        a12 = st.number_input("a₁₂", value=0.0, key="a12_3x3")
        a22 = st.number_input("a₂₂", value=1.0, key="a22_3x3")
        a32 = st.number_input("a₃₂", value=0.0, key="a32_3x3")
    
    with col3:
        a13 = st.number_input("a₁₃", value=0.0, key="a13_3x3")
        a23 = st.number_input("a₂₃", value=0.0, key="a23_3x3")
        a33 = st.number_input("a₃₃", value=1.0, key="a33_3x3")
    
    # Crear matriz
    matriz = np.array([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])
    
    # Mostrar matriz original
    st.write("**Matriz original:**")
    df_original = pd.DataFrame(matriz, index=['Fila 1', 'Fila 2', 'Fila 3'], 
                              columns=['Col 1', 'Col 2', 'Col 3'])
    st.dataframe(df_original, use_container_width=True)
    
    # Calcular inversa
    if st.button("🔢 Calcular Inversa", key="calc_inv_3x3"):
        try:
            # Verificar si es invertible
            det = np.linalg.det(matriz)
            st.write(f"**Determinante:** {det:.6f}")
            
            if abs(det) < 1e-10:
                st.error("❌ La matriz no es invertible (determinante ≈ 0)")
            else:
                inversa = np.linalg.inv(matriz)
                
                st.success("✅ Matriz invertible")
                
                # Mostrar inversa
                st.write("**Matriz inversa:**")
                df_inversa = pd.DataFrame(inversa, index=['Fila 1', 'Fila 2', 'Fila 3'], 
                                        columns=['Col 1', 'Col 2', 'Col 3'])
                st.dataframe(df_inversa, use_container_width=True)
                
                # Verificar resultado
                identidad = np.dot(matriz, inversa)
                st.write("**Verificación (A × A⁻¹):**")
                df_verificacion = pd.DataFrame(identidad, index=['Fila 1', 'Fila 2', 'Fila 3'], 
                                             columns=['Col 1', 'Col 2', 'Col 3'])
                st.dataframe(df_verificacion, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error al calcular la inversa: {str(e)}")

def render_matriz_personalizada():
    """Renderiza la calculadora para matrices personalizadas"""
    st.subheader("📐 Matriz Personalizada")
    
    # Seleccionar tamaño
    filas = st.number_input("Número de filas:", min_value=2, max_value=10, value=3)
    columnas = st.number_input("Número de columnas:", min_value=2, max_value=10, value=3)
    
    if filas != columnas:
        st.warning("⚠️ Para calcular la inversa, la matriz debe ser cuadrada (mismo número de filas y columnas)")
        return
    
    st.markdown(f"Ingresa los elementos de la matriz {filas}x{columnas}:")
    
    # Crear matriz con inputs
    matriz = np.zeros((filas, columnas))
    
    for i in range(filas):
        cols = st.columns(columnas)
        for j in range(columnas):
            with cols[j]:
                matriz[i, j] = st.number_input(f"a{i+1}{j+1}", value=1.0 if i == j else 0.0, 
                                             key=f"a{i+1}{j+1}_custom")
    
    # Mostrar matriz
    st.write("**Matriz ingresada:**")
    df_original = pd.DataFrame(matriz, 
                              index=[f'Fila {i+1}' for i in range(filas)],
                              columns=[f'Col {j+1}' for j in range(columnas)])
    st.dataframe(df_original, use_container_width=True)
    
    # Calcular inversa
    if st.button("🔢 Calcular Inversa", key="calc_inv_custom"):
        try:
            # Verificar si es invertible
            det = np.linalg.det(matriz)
            st.write(f"**Determinante:** {det:.6f}")
            
            if abs(det) < 1e-10:
                st.error("❌ La matriz no es invertible (determinante ≈ 0)")
            else:
                inversa = np.linalg.inv(matriz)
                
                st.success("✅ Matriz invertible")
                
                # Mostrar inversa
                st.write("**Matriz inversa:**")
                df_inversa = pd.DataFrame(inversa,
                                        index=[f'Fila {i+1}' for i in range(filas)],
                                        columns=[f'Col {j+1}' for j in range(columnas)])
                st.dataframe(df_inversa, use_container_width=True)
                
                # Verificar resultado
                identidad = np.dot(matriz, inversa)
                st.write("**Verificación (A × A⁻¹):**")
                df_verificacion = pd.DataFrame(identidad,
                                             index=[f'Fila {i+1}' for i in range(filas)],
                                             columns=[f'Col {j+1}' for j in range(columnas)])
                st.dataframe(df_verificacion, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error al calcular la inversa: {str(e)}")

def render_matriz_archivo():
    """Renderiza la calculadora para matrices desde archivo"""
    st.subheader("📁 Matriz desde Archivo")
    
    st.markdown("""
    Sube un archivo CSV con tu matriz. El archivo debe contener solo números separados por comas.
    """)
    
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Leer archivo
            df = pd.read_csv(uploaded_file, header=None)
            matriz = df.values
            
            st.write("**Matriz cargada:**")
            st.dataframe(df, use_container_width=True)
            
            # Verificar si es cuadrada
            if matriz.shape[0] != matriz.shape[1]:
                st.error("❌ La matriz debe ser cuadrada para calcular su inversa")
                return
            
            # Calcular inversa
            if st.button("🔢 Calcular Inversa", key="calc_inv_file"):
                try:
                    # Verificar si es invertible
                    det = np.linalg.det(matriz)
                    st.write(f"**Determinante:** {det:.6f}")
                    
                    if abs(det) < 1e-10:
                        st.error("❌ La matriz no es invertible (determinante ≈ 0)")
                    else:
                        inversa = np.linalg.inv(matriz)
                        
                        st.success("✅ Matriz invertible")
                        
                        # Mostrar inversa
                        st.write("**Matriz inversa:**")
                        df_inversa = pd.DataFrame(inversa)
                        st.dataframe(df_inversa, use_container_width=True)
                        
                        # Verificar resultado
                        identidad = np.dot(matriz, inversa)
                        st.write("**Verificación (A × A⁻¹):**")
                        df_verificacion = pd.DataFrame(identidad)
                        st.dataframe(df_verificacion, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"❌ Error al calcular la inversa: {str(e)}")
                    
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {str(e)}")
    
    # Ejemplo de formato
    st.subheader("📝 Ejemplo de Formato de Archivo")
    st.markdown("""
    **Formato CSV esperado:**
    ```
    1,0,0
    0,1,0
    0,0,1
    ```
    
    Esto representa la matriz identidad 3x3.
    """)
