import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.series_temporales import predecir_arima, calcular_metricas

def render():
    st.header("🔮 Predicciones ARIMA")
    st.markdown("""
    **Genera predicciones** usando el modelo ARIMA entrenado para predecir ventas futuras.
    Las predicciones incluyen intervalos de confianza para evaluar la incertidumbre.
    """)
    
    # Verificar si hay modelo entrenado
    if not st.session_state.get('modelo_entrenado', False):
        st.warning("⚠️ Primero debes entrenar un modelo ARIMA en la sección 'Entrenar Modelo'")
        return
    
    modelo = st.session_state['modelo_arima']
    parametros = st.session_state['parametros_arima']
    datos = st.session_state['datos_ventas']
    
    st.subheader("⚙️ Configuración de Predicciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_periodos = st.number_input("Períodos a predecir", min_value=1, max_value=100, value=10, step=1)
    
    with col2:
        incluir_intervalos = st.checkbox("Incluir intervalos de confianza", value=True)
    
    if st.button("Generar Predicciones", key="generar_predicciones"):
        with st.spinner("Generando predicciones..."):
            # Generar predicciones
            predicciones, mensaje = predecir_arima(modelo, n_periodos)
            
            if predicciones is not None:
                st.success(f"✅ {mensaje}")
                
                # Guardar predicciones en session_state
                st.session_state['predicciones_arima'] = predicciones
                st.session_state['n_periodos_pred'] = n_periodos
                st.session_state['predicciones_generadas'] = True
                
                # Mostrar predicciones en tabla
                st.subheader("📊 Predicciones Generadas")
                
                # Crear fechas futuras
                ultima_fecha = datos.index[-1]
                fechas_futuras = pd.date_range(start=ultima_fecha, periods=n_periodos+1, freq='D')[1:]
                
                df_predicciones = pd.DataFrame({
                    'Fecha': fechas_futuras,
                    'Predicción': predicciones['prediccion']
                })
                
                if incluir_intervalos:
                    df_predicciones['Límite Inferior'] = predicciones['intervalo_inferior']
                    df_predicciones['Límite Superior'] = predicciones['intervalo_superior']
                
                st.dataframe(df_predicciones, use_container_width=True)
                
                # Gráfico de predicciones
                st.subheader("📈 Gráfico de Predicciones")
                
                fig = go.Figure()
                
                # Serie original
                fig.add_trace(go.Scatter(
                    x=datos.index,
                    y=datos.values,
                    mode='lines',
                    name='Datos Históricos',
                    line=dict(width=2, color='#3498db')
                ))
                
                # Predicciones
                fig.add_trace(go.Scatter(
                    x=fechas_futuras,
                    y=predicciones['prediccion'],
                    mode='lines',
                    name='Predicciones',
                    line=dict(width=2, color='#e74c3c', dash='dash')
                ))
                
                # Intervalos de confianza
                if incluir_intervalos:
                    fig.add_trace(go.Scatter(
                        x=fechas_futuras,
                        y=predicciones['intervalo_superior'],
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=fechas_futuras,
                        y=predicciones['intervalo_inferior'],
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(231, 76, 60, 0.2)',
                        name='Intervalo de Confianza 95%'
                    ))
                
                fig.update_layout(
                    title=f"Predicciones ARIMA{parametros} - {n_periodos} períodos",
                    xaxis_title="Fecha",
                    yaxis_title="Ventas ($)",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas de predicciones
                st.subheader("📊 Estadísticas de Predicciones")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Predicción Promedio", f"${predicciones['prediccion'].mean():,.0f}")
                with col2:
                    st.metric("Predicción Máxima", f"${predicciones['prediccion'].max():,.0f}")
                with col3:
                    st.metric("Predicción Mínima", f"${predicciones['prediccion'].min():,.0f}")
                with col4:
                    st.metric("Desviación Estándar", f"${predicciones['prediccion'].std():,.0f}")
                
                # Análisis de tendencia en predicciones
                if n_periodos >= 2:
                    st.subheader("📈 Análisis de Tendencia en Predicciones")
                    
                    tendencia_pred = (predicciones['prediccion'].iloc[-1] - predicciones['prediccion'].iloc[0]) / n_periodos
                    crecimiento_pred = (tendencia_pred / predicciones['prediccion'].iloc[0]) * 100
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Tendencia Diaria", f"${tendencia_pred:,.0f}")
                    with col2:
                        st.metric("Crecimiento Total", f"{crecimiento_pred:.1f}%")
                    
                    if tendencia_pred > 0:
                        st.success("📈 **Tendencia Creciente** - Las ventas están aumentando")
                    elif tendencia_pred < 0:
                        st.warning("📉 **Tendencia Decreciente** - Las ventas están disminuyendo")
                    else:
                        st.info("📊 **Tendencia Estable** - Las ventas se mantienen constantes")
                
                # Recomendaciones
                st.subheader("💡 Recomendaciones")
                
                pred_promedio = predicciones['prediccion'].mean()
                hist_promedio = datos.mean()
                
                if pred_promedio > hist_promedio * 1.1:
                    st.success("🚀 **Predicción Optimista** - Se espera un crecimiento significativo")
                elif pred_promedio < hist_promedio * 0.9:
                    st.warning("⚠️ **Predicción Pesimista** - Se espera una disminución")
                else:
                    st.info("📊 **Predicción Estable** - Se mantiene el nivel actual")
                
                if incluir_intervalos:
                    rango_intervalos = (predicciones['intervalo_superior'] - predicciones['intervalo_inferior']).mean()
                    if rango_intervalos > pred_promedio * 0.2:
                        st.warning("⚠️ **Alta Incertidumbre** - Los intervalos de confianza son amplios")
                    else:
                        st.success("✅ **Baja Incertidumbre** - Los intervalos de confianza son estrechos")
                
            else:
                st.error(f"❌ {mensaje}")
    
    # Mostrar información sobre predicciones si no hay predicciones generadas
    if not st.session_state.get('predicciones_generadas', False):
        st.subheader("📚 ¿Qué son las Predicciones ARIMA?")
        st.markdown("""
        **Las predicciones ARIMA** utilizan el patrón histórico de la serie temporal para predecir valores futuros.
        
        **Componentes de las Predicciones:**
        - **Valor Punto:** La predicción más probable
        - **Intervalo de Confianza:** Rango de valores probables (95% de confianza)
        - **Incertidumbre:** Qué tan confiable es la predicción
        
        **Factores que Afectan la Precisión:**
        - **Calidad del modelo:** Parámetros (p,d,q) bien seleccionados
        - **Estacionariedad:** La serie debe ser estacionaria
        - **Patrones estables:** Los patrones históricos deben mantenerse
        
        **Limitaciones:**
        - **Corto plazo:** Más precisas para predicciones cercanas
        - **Cambios estructurales:** No predice cambios abruptos
        - **Eventos externos:** No considera factores externos
        """)
