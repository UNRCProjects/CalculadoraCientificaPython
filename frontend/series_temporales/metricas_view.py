import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.series_temporales import calcular_metricas

def render():
    st.header("📈 Métricas de Evaluación")
    st.markdown("""
    **Evalúa el rendimiento** del modelo ARIMA usando diferentes métricas estadísticas.
    Estas métricas te ayudan a entender qué tan bien predice el modelo.
    """)
    
    # Verificar si hay predicciones disponibles
    if not st.session_state.get('predicciones_generadas', False):
        st.warning("⚠️ Primero debes generar predicciones en la sección 'Predicciones'")
        return
    
    predicciones = st.session_state['predicciones_arima']
    datos = st.session_state['datos_ventas']
    n_periodos = st.session_state['n_periodos_pred']
    
    # Usar los últimos n_periodos de datos reales para comparar
    datos_reales = datos.tail(n_periodos)
    datos_predichos = predicciones['prediccion']
    
    st.subheader("📊 Métricas de Precisión")
    
    if st.button("Calcular Métricas", key="calcular_metricas"):
        with st.spinner("Calculando métricas..."):
            # Calcular métricas
            metricas = calcular_metricas(datos_reales, datos_predichos)
            
            # Mostrar métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("RMSE", f"{metricas['RMSE']:.2f}")
                st.caption("Root Mean Square Error")
            with col2:
                st.metric("MAE", f"{metricas['MAE']:.2f}")
                st.caption("Mean Absolute Error")
            with col3:
                st.metric("MAPE", f"{metricas['MAPE']:.1f}%")
                st.caption("Mean Absolute Percentage Error")
            with col4:
                st.metric("MSE", f"{metricas['MSE']:.2f}")
                st.caption("Mean Square Error")
            
            # Guardar métricas en session_state
            st.session_state['metricas_arima'] = metricas
            st.session_state['metricas_calculadas'] = True
            
            # Interpretación de métricas
            st.subheader("💡 Interpretación de Métricas")
            
            # RMSE
            if metricas['RMSE'] < datos_reales.std():
                st.success("✅ **RMSE Bueno** - El error es menor que la variabilidad natural")
            elif metricas['RMSE'] < datos_reales.std() * 2:
                st.warning("⚠️ **RMSE Moderado** - El error es aceptable")
            else:
                st.error("❌ **RMSE Alto** - El modelo necesita mejoras")
            
            # MAPE
            if metricas['MAPE'] < 5:
                st.success("✅ **MAPE Excelente** - Error menor al 5%")
            elif metricas['MAPE'] < 10:
                st.success("✅ **MAPE Bueno** - Error menor al 10%")
            elif metricas['MAPE'] < 20:
                st.warning("⚠️ **MAPE Moderado** - Error entre 10-20%")
            else:
                st.error("❌ **MAPE Alto** - Error mayor al 20%")
            
            # MAE
            if metricas['MAE'] < datos_reales.mean() * 0.1:
                st.success("✅ **MAE Excelente** - Error menor al 10% del promedio")
            elif metricas['MAE'] < datos_reales.mean() * 0.2:
                st.warning("⚠️ **MAE Moderado** - Error entre 10-20% del promedio")
            else:
                st.error("❌ **MAE Alto** - Error mayor al 20% del promedio")
            
            # Gráfico de comparación
            st.subheader("📊 Comparación: Real vs Predicho")
            
            fig = go.Figure()
            
            # Datos reales
            fig.add_trace(go.Scatter(
                x=datos_reales.index,
                y=datos_reales.values,
                mode='lines+markers',
                name='Datos Reales',
                line=dict(width=2, color='#3498db'),
                marker=dict(size=6)
            ))
            
            # Datos predichos
            fechas_pred = pd.date_range(start=datos_reales.index[0], periods=len(datos_predichos), freq='D')
            fig.add_trace(go.Scatter(
                x=fechas_pred,
                y=datos_predichos.values,
                mode='lines+markers',
                name='Predicciones',
                line=dict(width=2, color='#e74c3c', dash='dash'),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title="Comparación: Datos Reales vs Predicciones",
                xaxis_title="Fecha",
                yaxis_title="Ventas ($)",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Análisis de errores
            st.subheader("🔍 Análisis de Errores")
            
            errores = datos_reales.values - datos_predichos.values
            errores_abs = np.abs(errores)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Distribución de Errores:**")
                st.markdown(f"• Error promedio: ${np.mean(errores):,.0f}")
                st.markdown(f"• Error máximo: ${np.max(errores_abs):,.0f}")
                st.markdown(f"• Error mínimo: ${np.min(errores_abs):,.0f}")
                st.markdown(f"• Desviación estándar: ${np.std(errores):,.0f}")
            
            with col2:
                st.markdown("**Calidad del Modelo:**")
                if metricas['MAPE'] < 10:
                    st.success("🟢 **Excelente**")
                elif metricas['MAPE'] < 20:
                    st.warning("🟡 **Bueno**")
                else:
                    st.error("🔴 **Necesita Mejoras**")
                
                if metricas['RMSE'] < datos_reales.std():
                    st.success("🟢 **Preciso**")
                else:
                    st.warning("🟡 **Moderado**")
            
            # Recomendaciones
            st.subheader("🎯 Recomendaciones")
            
            if metricas['MAPE'] < 10 and metricas['RMSE'] < datos_reales.std():
                st.success("""
                **🎉 Modelo Excelente:**
                - El modelo tiene muy buena precisión
                - Puedes confiar en las predicciones
                - Considera usar este modelo para decisiones de negocio
                """)
            elif metricas['MAPE'] < 20:
                st.warning("""
                **⚠️ Modelo Aceptable:**
                - El modelo tiene precisión moderada
                - Úsalo con precaución para decisiones importantes
                - Considera ajustar los parámetros (p,d,q)
                """)
            else:
                st.error("""
                **❌ Modelo Necesita Mejoras:**
                - El modelo tiene baja precisión
                - No confíes en las predicciones
                - Prueba diferentes parámetros o métodos
                - Considera más datos de entrenamiento
                """)
    
    # Mostrar información sobre métricas si no están calculadas
    if not st.session_state.get('metricas_calculadas', False):
        st.subheader("📚 ¿Qué son las Métricas de Evaluación?")
        st.markdown("""
        **Las métricas de evaluación** miden qué tan bien predice el modelo:
        
        **RMSE (Root Mean Square Error):**
        - Mide la raíz cuadrada del error cuadrático medio
        - Penaliza más los errores grandes
        - Misma unidad que los datos originales
        
        **MAE (Mean Absolute Error):**
        - Mide el error absoluto promedio
        - No penaliza más los errores grandes
        - Más fácil de interpretar
        
        **MAPE (Mean Absolute Percentage Error):**
        - Mide el error porcentual promedio
        - Permite comparar entre diferentes escalas
        - Valores menores al 10% se consideran buenos
        
        **MSE (Mean Square Error):**
        - Mide el error cuadrático medio
        - Penaliza mucho los errores grandes
        - Usado para optimización del modelo
        """)
