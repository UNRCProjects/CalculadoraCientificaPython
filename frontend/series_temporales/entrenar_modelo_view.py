import streamlit as st
import pandas as pd
from backend.series_temporales import encontrar_parametros_arima, entrenar_arima

def render():
    st.header("🤖 Entrenar Modelo ARIMA")
    st.markdown("""
    **Modelo ARIMA:** AutoRegressive Integrated Moving Average
    - **AR (p):** Componente autorregresivo
    - **I (d):** Componente integrado (diferenciación)
    - **MA (q):** Componente de media móvil
    """)
    
    # Verificar si hay datos disponibles
    if 'datos_ventas' not in st.session_state or not st.session_state.get('datos_generados', False):
        st.warning("⚠️ Primero debes generar datos de ventas en la sección 'Generar Datos'")
        return
    
    datos = st.session_state['datos_ventas']
    
    st.subheader("⚙️ Configuración del Modelo")
    
    # Opciones de parámetros
    col1, col2 = st.columns(2)
    
    with col1:
        auto_parametros = st.checkbox("Selección automática de parámetros", value=True)
    
    with col2:
        if not auto_parametros:
            st.info("Configuración manual de parámetros")
    
    if not auto_parametros:
        st.subheader("📊 Parámetros Manuales")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            p = st.number_input("p (AR)", min_value=0, max_value=10, value=1, step=1)
        with col2:
            d = st.number_input("d (I)", min_value=0, max_value=3, value=1, step=1)
        with col3:
            q = st.number_input("q (MA)", min_value=0, max_value=10, value=1, step=1)
    else:
        p, d, q = None, None, None
    
    if st.button("Entrenar Modelo ARIMA", key="entrenar_modelo"):
        with st.spinner("Entrenando modelo ARIMA..."):
            if auto_parametros:
                # Encontrar parámetros óptimos
                st.info("🔍 Buscando parámetros óptimos...")
                parametros, aic = encontrar_parametros_arima(datos)
                
                if parametros:
                    p, d, q = parametros
                    st.success(f"✅ Parámetros óptimos encontrados: ARIMA({p},{d},{q})")
                    st.info(f"📊 AIC: {aic:.2f}")
                else:
                    st.error("❌ No se pudieron encontrar parámetros óptimos")
                    return
            else:
                st.info(f"🔧 Usando parámetros manuales: ARIMA({p},{d},{q})")
            
            # Entrenar modelo
            modelo, mensaje = entrenar_arima(datos, p, d, q)
            
            if modelo is not None:
                st.success(f"✅ {mensaje}")
                
                # Guardar modelo en session_state
                st.session_state['modelo_arima'] = modelo
                st.session_state['parametros_arima'] = (p, d, q)
                st.session_state['modelo_entrenado'] = True
                
                # Mostrar resumen del modelo
                st.subheader("📊 Resumen del Modelo")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("p (AR)", p)
                with col2:
                    st.metric("d (I)", d)
                with col3:
                    st.metric("q (MA)", q)
                
                # Métricas del modelo
                st.subheader("📈 Métricas del Modelo")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("AIC", f"{modelo.aic:.2f}")
                with col2:
                    st.metric("BIC", f"{modelo.bic:.2f}")
                with col3:
                    st.metric("Log-Likelihood", f"{modelo.llf:.2f}")
                with col4:
                    st.metric("Observaciones", f"{modelo.nobs}")
                
                # Interpretación de parámetros
                st.subheader("💡 Interpretación de Parámetros")
                
                interpretacion = []
                
                if p > 0:
                    interpretacion.append(f"**AR({p}):** El modelo usa {p} valores pasados para predecir")
                else:
                    interpretacion.append("**AR(0):** No hay componente autorregresivo")
                
                if d > 0:
                    interpretacion.append(f"**I({d}):** Se aplicó diferenciación {d} vez(es) para hacer la serie estacionaria")
                else:
                    interpretacion.append("**I(0):** No se necesitó diferenciación")
                
                if q > 0:
                    interpretacion.append(f"**MA({q}):** El modelo usa {q} errores pasados para predecir")
                else:
                    interpretacion.append("**MA(0):** No hay componente de media móvil")
                
                for interp in interpretacion:
                    st.markdown(f"• {interp}")
                
                # Recomendaciones
                st.subheader("🎯 Recomendaciones")
                
                if modelo.aic < 1000:
                    st.success("✅ **Modelo con buen ajuste** - AIC bajo indica buen ajuste")
                elif modelo.aic < 2000:
                    st.warning("⚠️ **Modelo con ajuste moderado** - Considera probar otros parámetros")
                else:
                    st.error("❌ **Modelo con ajuste pobre** - Revisa los parámetros")
                
                if d == 0:
                    st.info("💡 **Sin diferenciación** - La serie ya era estacionaria")
                elif d == 1:
                    st.info("💡 **Una diferenciación** - Se necesitó una diferenciación para estacionarizar")
                else:
                    st.info("💡 **Múltiples diferenciaciones** - Se necesitaron {d} diferenciaciones")
                
            else:
                st.error(f"❌ {mensaje}")
    
    # Mostrar información sobre ARIMA si no hay modelo entrenado
    if not st.session_state.get('modelo_entrenado', False):
        st.subheader("📚 ¿Qué es ARIMA?")
        st.markdown("""
        **ARIMA** es un modelo estadístico para series temporales que combina:
        
        - **AR (AutoRegresivo):** Usa valores pasados de la serie
        - **I (Integrado):** Aplica diferenciación para hacer la serie estacionaria
        - **MA (Media Móvil):** Usa errores de predicción pasados
        
        **Selección de Parámetros:**
        - **p:** Número de términos autorregresivos
        - **d:** Número de diferenciaciones necesarias
        - **q:** Número de términos de media móvil
        
        **Criterio AIC:** Se usa para seleccionar el mejor modelo (menor AIC = mejor modelo)
        """)
