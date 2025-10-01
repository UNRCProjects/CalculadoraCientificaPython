import streamlit as st
import pandas as pd
import numpy as np
from backend.investigacion_operaciones import transportation_problem

def render():
    st.header("Problema de Transporte")
    st.markdown("""
    **Definición:** El problema de transporte consiste en determinar la cantidad de producto que debe 
    enviarse desde cada origen hasta cada destino para minimizar el costo total del transporte, 
    respetando las ofertas y demandas.
    """)
    
    st.subheader("Configuración del Problema")
    
    # Dimensiones del problema
    col1, col2 = st.columns(2)
    with col1:
        num_origins = st.number_input("Número de orígenes", min_value=2, max_value=5, value=2, step=1)
    with col2:
        num_destinations = st.number_input("Número de destinos", min_value=2, max_value=5, value=2, step=1)
    
    # Matriz de costos
    st.subheader("Matriz de Costos")
    st.write("Ingresa los costos de transporte de cada origen a cada destino:")
    
    cost_matrix = []
    for i in range(num_origins):
        st.write(f"**Origen {i+1}:**")
        cols = st.columns(num_destinations)
        row = []
        for j in range(num_destinations):
            with cols[j]:
                cost = st.number_input(f"Destino {j+1}", value=1.0, min_value=0.0, step=0.1, key=f"cost_{i}_{j}")
                row.append(cost)
        cost_matrix.append(row)
    
    # Mostrar matriz de costos
    st.subheader("Matriz de Costos")
    cost_df = pd.DataFrame(cost_matrix, 
                         index=[f'Origen {i+1}' for i in range(num_origins)],
                         columns=[f'Destino {j+1}' for j in range(num_destinations)])
    st.dataframe(cost_df, use_container_width=True)
    
    # Ofertas
    st.subheader("Ofertas (Capacidades de Origen)")
    supply = []
    cols = st.columns(num_origins)
    for i in range(num_origins):
        with cols[i]:
            offer = st.number_input(f"Origen {i+1}", value=10.0, min_value=0.0, step=1.0, key=f"supply_{i}")
            supply.append(offer)
    
    # Demandas
    st.subheader("Demandas (Requerimientos de Destino)")
    demand = []
    cols = st.columns(num_destinations)
    for i in range(num_destinations):
        with cols[i]:
            req = st.number_input(f"Destino {i+1}", value=10.0, min_value=0.0, step=1.0, key=f"demand_{i}")
            demand.append(req)
    
    # Verificar balance
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Oferta", f"{total_supply:.1f}")
    with col2:
        st.metric("Total Demanda", f"{total_demand:.1f}")
    
    if abs(total_supply - total_demand) > 0.01:
        st.warning("⚠️ El problema no está balanceado. La oferta y demanda deben ser iguales.")
    
    # Botón para resolver
    if st.button("Resolver Problema de Transporte"):
        try:
            result = transportation_problem(cost_matrix, supply, demand)
            
            if result['success']:
                st.success("✅ Problema resuelto exitosamente!")
                
                # Mostrar costo total
                st.metric("Costo Total Mínimo", f"${result['total_cost']:.2f}")
                
                # Mostrar matriz de solución
                st.subheader("Solución Óptima")
                st.write("Cantidades a transportar de cada origen a cada destino:")
                
                solution_df = pd.DataFrame(result['solution_matrix'],
                                        index=[f'Origen {i+1}' for i in range(num_origins)],
                                        columns=[f'Destino {j+1}' for j in range(num_destinations)])
                st.dataframe(solution_df, use_container_width=True)
                
                # Análisis detallado
                st.subheader("Análisis Detallado")
                
                # Verificar restricciones
                st.write("**Verificación de Ofertas:**")
                for i in range(num_origins):
                    total_sent = sum(result['solution_matrix'][i])
                    st.write(f"Origen {i+1}: {total_sent:.1f} / {supply[i]:.1f} ✓" if abs(total_sent - supply[i]) < 0.01 else f"Origen {i+1}: {total_sent:.1f} / {supply[i]:.1f} ✗")
                
                st.write("**Verificación de Demandas:**")
                for j in range(num_destinations):
                    total_received = sum(result['solution_matrix'][i][j] for i in range(num_origins))
                    st.write(f"Destino {j+1}: {total_received:.1f} / {demand[j]:.1f} ✓" if abs(total_received - demand[j]) < 0.01 else f"Destino {j+1}: {total_received:.1f} / {demand[j]:.1f} ✗")
                
            else:
                st.error(f"❌ Error al resolver el problema: {result.get('error', 'Error desconocido')}")
                
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
    
    # Información adicional
    with st.expander("ℹ️ Información sobre el Problema de Transporte"):
        st.markdown("""
        **¿Qué es el Problema de Transporte?**
        
        Es un problema de optimización que busca minimizar el costo total de transporte de productos 
        desde varios orígenes hasta varios destinos, respetando las capacidades de oferta y las demandas.
        
        **Características:**
        - **Objetivo:** Minimizar el costo total de transporte
        - **Restricciones:** Ofertas de origen y demandas de destino
        - **Variables:** Cantidades a transportar entre cada par origen-destino
        
        **Aplicaciones:**
        - Distribución de productos
        - Asignación de recursos
        - Planificación de rutas
        - Optimización de cadenas de suministro
        
        **Condición de Balance:**
        El problema debe estar balanceado: ∑Ofertas = ∑Demandas
        """)