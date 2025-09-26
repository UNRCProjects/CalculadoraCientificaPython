import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.series_temporales import generar_datos_ventas, obtener_resumen_ventas

def render():
    st.header("📊 Generar Datos de Ventas")
    st.markdown("""
    **Genera datos de ventas simulados** con patrones realistas para practicar análisis de series temporales.
    Los datos incluyen tendencia, estacionalidad, eventos especiales y variabilidad natural.
    """)
    
    # Configuración
    col1, col2 = st.columns(2)
    
    with col1:
        n_dias = st.number_input("Número de días", min_value=30, max_value=365, value=180, step=1)
    
    with col2:
        tipo_datos = st.selectbox("Tipo de datos", ["Ventas realistas", "Ventas simples"])
    
    if st.button("Generar Datos", key="generar_datos"):
        with st.spinner("Generando datos de ventas..."):
            # Generar datos
            datos = generar_datos_ventas(n_dias)
            
            # Guardar en session_state
            st.session_state['datos_ventas'] = datos
            st.session_state['datos_generados'] = True
            
            st.success(f"✅ Datos generados exitosamente: {len(datos)} días")
    
    # Mostrar datos si están disponibles
    if 'datos_ventas' in st.session_state and st.session_state.get('datos_generados', False):
        datos = st.session_state['datos_ventas']
        
        # Resumen estadístico
        st.subheader("📈 Resumen de Ventas")
        resumen = obtener_resumen_ventas(datos)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Ventas Totales", f"${resumen['total_ventas']:,.0f}")
        with col2:
            st.metric("📊 Promedio Diario", f"${resumen['promedio_diario']:,.0f}")
        with col3:
            st.metric("📈 Crecimiento", f"{resumen['crecimiento_total']:.1f}%")
        with col4:
            st.metric("📊 Volatilidad", f"{resumen['volatilidad']:.1f}%")
        
        # Gráfico de la serie temporal
        st.subheader("📊 Serie Temporal de Ventas")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=datos.index,
            y=datos.values,
            mode='lines',
            name='Ventas',
            line=dict(width=2, color='#3498db')
        ))
        
        fig.update_layout(
            title="Ventas Diarias",
            xaxis_title="Fecha",
            yaxis_title="Ventas ($)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análisis por día de la semana
        st.subheader("📅 Análisis por Día de la Semana")
        
        ventas_semanal = datos.groupby(datos.index.dayofweek).mean()
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_semanal = go.Figure()
            fig_semanal.add_trace(go.Bar(
                x=dias_semana,
                y=ventas_semanal.values,
                marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff']
            ))
            fig_semanal.update_layout(
                title="Ventas Promedio por Día de la Semana",
                xaxis_title="Día de la Semana",
                yaxis_title="Ventas ($)",
                height=400
            )
            st.plotly_chart(fig_semanal, use_container_width=True)
        
        with col2:
            st.markdown("**Ranking de Días:**")
            ranking = ventas_semanal.sort_values(ascending=False)
            for i, (dia_idx, ventas) in enumerate(ranking.items(), 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📊"
                st.markdown(f"{emoji} **{dias_semana[dia_idx]}**: ${ventas:,.0f}")
        
        # Análisis mensual
        if len(datos) >= 30:
            st.subheader("📊 Análisis Mensual")
            ventas_mensuales = datos.resample('M').sum()
            ventas_mensuales.index = ventas_mensuales.index.strftime('%B %Y')
            
            fig_mensual = go.Figure()
            fig_mensual.add_trace(go.Bar(
                x=ventas_mensuales.index,
                y=ventas_mensuales.values,
                marker_color='#3498db'
            ))
            fig_mensual.update_layout(
                title="Ventas Totales por Mes",
                xaxis_title="Mes",
                yaxis_title="Ventas ($)",
                height=400
            )
            st.plotly_chart(fig_mensual, use_container_width=True)
        
        # Tabla de datos
        st.subheader("📋 Datos Generados")
        if st.checkbox("Mostrar tabla de datos"):
            df_mostrar = pd.DataFrame({
                'Fecha': datos.index,
                'Ventas': datos.values
            })
            st.dataframe(df_mostrar, use_container_width=True)
