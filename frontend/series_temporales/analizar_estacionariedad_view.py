import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.series_temporales import analizar_estacionariedad

def render():
    st.header("🔍 Análisis de Estacionariedad")
    st.markdown("""
    **Test de Estacionariedad (ADF):** Determina si una serie temporal es estacionaria.
    Una serie estacionaria tiene propiedades estadísticas constantes en el tiempo.
    """)
    
    # Verificar si hay datos disponibles
    if 'datos_ventas' not in st.session_state or not st.session_state.get('datos_generados', False):
        st.warning("⚠️ Primero debes generar datos de ventas en la sección 'Generar Datos'")
        return
    
    datos = st.session_state['datos_ventas']
    
    st.subheader("📊 Serie Temporal Original")
    
    # Mostrar la serie original
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=datos.index,
        y=datos.values,
        mode='lines',
        name='Ventas Originales',
        line=dict(width=2, color='#3498db')
    ))
    
    fig.update_layout(
        title="Serie Temporal de Ventas",
        xaxis_title="Fecha",
        yaxis_title="Ventas ($)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Realizar Test de Estacionariedad", key="test_estacionariedad"):
        with st.spinner("Analizando estacionariedad..."):
            # Realizar test ADF
            resultado = analizar_estacionariedad(datos)
            
            # Mostrar resultados
            st.subheader("📈 Resultados del Test ADF")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Estadístico ADF", f"{resultado['estadistico_adf']:.4f}")
                st.metric("P-valor", f"{resultado['p_valor']:.4f}")
            
            with col2:
                if resultado['es_estacionaria']:
                    st.success("✅ **Serie Estacionaria**")
                    st.info("La serie es estacionaria. No necesita diferenciación.")
                else:
                    st.warning("⚠️ **Serie No Estacionaria**")
                    st.info("La serie necesita diferenciación para ser estacionaria.")
            
            # Valores críticos
            st.subheader("📊 Valores Críticos")
            valores_criticos = pd.DataFrame({
                'Nivel de Significancia': ['1%', '5%', '10%'],
                'Valor Crítico': [resultado['valores_criticos']['1%'], 
                                resultado['valores_criticos']['5%'], 
                                resultado['valores_criticos']['10%']]
            })
            st.dataframe(valores_criticos, use_container_width=True)
            
            # Interpretación
            st.subheader("💡 Interpretación")
            if resultado['es_estacionaria']:
                st.success("""
                **La serie es estacionaria:**
                - El p-valor es menor a 0.05
                - Se puede proceder directamente con el modelo ARIMA
                - No se necesita diferenciación (d=0)
                """)
            else:
                st.warning("""
                **La serie no es estacionaria:**
                - El p-valor es mayor a 0.05
                - Se necesita aplicar diferenciación
                - El parámetro d del modelo ARIMA será mayor a 0
                """)
            
            # Mostrar serie diferenciada si no es estacionaria
            if not resultado['es_estacionaria']:
                st.subheader("📊 Serie Diferenciada (Primera Diferencia)")
                
                datos_diff = datos.diff().dropna()
                
                fig_diff = go.Figure()
                fig_diff.add_trace(go.Scatter(
                    x=datos_diff.index,
                    y=datos_diff.values,
                    mode='lines',
                    name='Primera Diferencia',
                    line=dict(width=2, color='#e74c3c')
                ))
                
                fig_diff.update_layout(
                    title="Serie Diferenciada (Primera Diferencia)",
                    xaxis_title="Fecha",
                    yaxis_title="Diferencia de Ventas ($)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig_diff, use_container_width=True)
                
                # Test de estacionariedad en la serie diferenciada
                if st.button("Test en Serie Diferenciada", key="test_diff"):
                    with st.spinner("Analizando serie diferenciada..."):
                        resultado_diff = analizar_estacionariedad(datos_diff)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Estadístico ADF (Diferenciada)", f"{resultado_diff['estadistico_adf']:.4f}")
                            st.metric("P-valor (Diferenciada)", f"{resultado_diff['p_valor']:.4f}")
                        
                        with col2:
                            if resultado_diff['es_estacionaria']:
                                st.success("✅ **Serie Diferenciada Estacionaria**")
                                st.info("d = 1 (una diferenciación)")
                            else:
                                st.warning("⚠️ **Aún No Estacionaria**")
                                st.info("Se necesita más diferenciación (d > 1)")
