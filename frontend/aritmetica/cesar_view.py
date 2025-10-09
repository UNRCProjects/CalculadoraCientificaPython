import streamlit as st
import string

def render():
    st.header("🔐 Cifrado de César")
    
    st.markdown("""
    ### ¿Qué es el Cifrado de César?
    
    El cifrado de César es uno de los métodos de cifrado más antiguos y simples. 
    Es un tipo de cifrado por sustitución en el que cada letra del texto original 
    es reemplazada por otra letra que se encuentra un número fijo de posiciones 
    más adelante en el alfabeto.
    """)
    
    # Ejemplo visual
    st.markdown("""
    **Ejemplo:** Si usamos un desplazamiento de 3:
    - A → D
    - B → E  
    - C → F
    - ... y así sucesivamente
    """)
    
    # Sección de cifrado
    st.subheader("🔒 Cifrar Texto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        texto_original = st.text_area(
            "Texto a cifrar:",
            value="HOLA MUNDO",
            height=100,
            help="Ingresa el texto que quieres cifrar"
        )
        
        desplazamiento = st.number_input(
            "Desplazamiento:",
            min_value=1,
            max_value=25,
            value=3,
            help="Número de posiciones a desplazar (1-25)"
        )
    
    with col2:
        if st.button("🔐 Cifrar", key="cifrar_btn"):
            if texto_original:
                texto_cifrado = cifrar_cesar(texto_original, desplazamiento)
                st.text_area("Texto cifrado:", value=texto_cifrado, height=100)
            else:
                st.warning("⚠️ Por favor ingresa un texto para cifrar")
    
    # Sección de descifrado
    st.subheader("🔓 Descifrar Texto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        texto_cifrado_input = st.text_area(
            "Texto cifrado:",
            value="",
            height=100,
            help="Ingresa el texto que quieres descifrar"
        )
        
        desplazamiento_descifrar = st.number_input(
            "Desplazamiento:",
            min_value=1,
            max_value=25,
            value=3,
            key="desplazamiento_descifrar",
            help="Número de posiciones que se usó para cifrar"
        )
    
    with col2:
        if st.button("🔓 Descifrar", key="descifrar_btn"):
            if texto_cifrado_input:
                texto_descifrado = descifrar_cesar(texto_cifrado_input, desplazamiento_descifrar)
                st.text_area("Texto descifrado:", value=texto_descifrado, height=100)
            else:
                st.warning("⚠️ Por favor ingresa un texto cifrado para descifrar")
    
    # Sección de análisis automático
    st.subheader("🔍 Análisis Automático")
    
    texto_analizar = st.text_input(
        "Texto para analizar:",
        value="",
        help="Ingresa un texto cifrado para intentar descifrarlo automáticamente"
    )
    
    if st.button("🔍 Analizar y Descifrar"):
        if texto_analizar:
            with st.spinner("Analizando texto..."):
                resultados = analizar_cesar(texto_analizar)
                
                st.write("**Posibles descifrados:**")
                for i, (desplazamiento, texto) in enumerate(resultados[:5], 1):
                    with st.expander(f"Opción {i}: Desplazamiento {desplazamiento}"):
                        st.write(f"**Texto descifrado:** {texto}")
                        if st.button(f"Seleccionar esta opción", key=f"seleccionar_{i}"):
                            st.session_state['texto_descifrado'] = texto
                            st.success("✅ Texto seleccionado")
        else:
            st.warning("⚠️ Por favor ingresa un texto para analizar")
    
    # Información adicional
    st.subheader("ℹ️ Información Adicional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Ventajas del Cifrado de César:**
        - ✅ Simple de entender e implementar
        - ✅ Rápido de usar
        - ✅ Históricamente importante
        """)
    
    with col2:
        st.markdown("""
        **Desventajas:**
        - ❌ Muy fácil de descifrar
        - ❌ Solo 25 claves posibles
        - ❌ Vulnerable a análisis de frecuencia
        """)
    
    # Ejemplo práctico
    st.subheader("📚 Ejemplo Práctico")
    
    st.markdown("""
    **Ejemplo histórico:** Julio César usaba un desplazamiento de 3 para comunicarse con sus generales.
    
    - **Texto original:** "ATACAR AL AMANECER"
    - **Desplazamiento:** 3
    - **Texto cifrado:** "DWDFDU DO DPDQHFHU"
    """)

def cifrar_cesar(texto, desplazamiento):
    """Cifra un texto usando el método de César"""
    resultado = ""
    
    for caracter in texto:
        if caracter.isalpha():
            # Determinar si es mayúscula o minúscula
            if caracter.isupper():
                # Para mayúsculas: A=65, Z=90
                codigo = ord(caracter) - ord('A')
                nuevo_codigo = (codigo + desplazamiento) % 26
                resultado += chr(nuevo_codigo + ord('A'))
            else:
                # Para minúsculas: a=97, z=122
                codigo = ord(caracter) - ord('a')
                nuevo_codigo = (codigo + desplazamiento) % 26
                resultado += chr(nuevo_codigo + ord('a'))
        else:
            # Mantener caracteres que no son letras
            resultado += caracter
    
    return resultado

def descifrar_cesar(texto_cifrado, desplazamiento):
    """Descifra un texto usando el método de César"""
    resultado = ""
    
    for caracter in texto_cifrado:
        if caracter.isalpha():
            # Determinar si es mayúscula o minúscula
            if caracter.isupper():
                # Para mayúsculas: A=65, Z=90
                codigo = ord(caracter) - ord('A')
                nuevo_codigo = (codigo - desplazamiento) % 26
                resultado += chr(nuevo_codigo + ord('A'))
            else:
                # Para minúsculas: a=97, z=122
                codigo = ord(caracter) - ord('a')
                nuevo_codigo = (codigo - desplazamiento) % 26
                resultado += chr(nuevo_codigo + ord('a'))
        else:
            # Mantener caracteres que no son letras
            resultado += caracter
    
    return resultado

def analizar_cesar(texto_cifrado):
    """Analiza un texto cifrado probando todos los desplazamientos posibles"""
    resultados = []
    
    for desplazamiento in range(1, 26):
        texto_descifrado = descifrar_cesar(texto_cifrado, desplazamiento)
        # Calcular un score basado en la frecuencia de letras comunes en español
        score = calcular_score_espanol(texto_descifrado)
        resultados.append((desplazamiento, texto_descifrado, score))
    
    # Ordenar por score (mayor score = más probable que sea correcto)
    resultados.sort(key=lambda x: x[2], reverse=True)
    
    return [(desplazamiento, texto) for desplazamiento, texto, score in resultados]

def calcular_score_espanol(texto):
    """Calcula un score basado en la frecuencia de letras comunes en español"""
    # Frecuencias aproximadas de letras en español
    frecuencias = {
        'E': 0.1368, 'A': 0.1253, 'O': 0.0868, 'I': 0.0701, 'S': 0.0718,
        'N': 0.0671, 'R': 0.0612, 'U': 0.0468, 'L': 0.0495, 'D': 0.0468,
        'T': 0.0392, 'C': 0.0392, 'P': 0.0316, 'M': 0.0316, 'B': 0.0141,
        'G': 0.0101, 'V': 0.0101, 'Y': 0.0101, 'Q': 0.0088, 'H': 0.0070,
        'F': 0.0053, 'J': 0.0044, 'Z': 0.0035, 'X': 0.0002, 'K': 0.0002,
        'W': 0.0002
    }
    
    score = 0
    texto_upper = texto.upper()
    
    for letra, frecuencia in frecuencias.items():
        count = texto_upper.count(letra)
        score += count * frecuencia
    
    return score
