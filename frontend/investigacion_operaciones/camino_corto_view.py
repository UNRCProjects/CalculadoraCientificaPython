import streamlit as st
import pandas as pd
import numpy as np
from backend.investigacion_operaciones import shortest_path

def render():
    st.header("Problema de Camino Más Corto")
    st.markdown("""
    **Definición:** El problema de camino más corto consiste en encontrar la ruta de menor costo 
    (distancia, tiempo, etc.) entre dos nodos en una red, donde cada arco tiene un costo asociado.
    """)
    
    st.subheader("Configuración de la Red")
    
    # Número de nodos
    num_nodes = st.number_input("Número de nodos", min_value=3, max_value=8, value=4, step=1)
    
    # Matriz de adyacencia
    st.subheader("Matriz de Adyacencia (Distancias)")
    st.write("Ingresa las distancias entre nodos (0 = sin conexión):")
    
    adjacency_matrix = []
    for i in range(num_nodes):
        st.write(f"**Desde nodo {i+1}:**")
        cols = st.columns(num_nodes)
        row = []
        for j in range(num_nodes):
            with cols[j]:
                if i == j:
                    distance = 0
                    st.write("0")
                else:
                    distance = st.number_input(f"Hacia nodo {j+1}", value=0.0, min_value=0.0, step=0.1, key=f"dist_{i}_{j}")
                row.append(distance)
        adjacency_matrix.append(row)
    
    # Mostrar matriz de adyacencia
    st.subheader("Matriz de Adyacencia")
    adj_df = pd.DataFrame(adjacency_matrix, 
                           index=[f'Nodo {i+1}' for i in range(num_nodes)],
                           columns=[f'Nodo {j+1}' for j in range(num_nodes)])
    st.dataframe(adj_df, use_container_width=True)
    
    # Nodos de inicio y destino
    st.subheader("Nodos de Inicio y Destino")
    col1, col2 = st.columns(2)
    with col1:
        start_node = st.selectbox("Nodo de inicio", range(num_nodes), format_func=lambda x: f"Nodo {x+1}")
    with col2:
        end_node = st.selectbox("Nodo de destino", range(num_nodes), format_func=lambda x: f"Nodo {x+1}")
    
    # Botón para resolver
    if st.button("Encontrar Camino Más Corto"):
        try:
            result = shortest_path(adjacency_matrix, start_node, end_node)
            
            if result['success']:
                st.success("✅ Camino encontrado exitosamente!")
                
                # Mostrar distancia total
                st.metric("Distancia Total", f"{result['distance']:.2f}")
                
                # Mostrar camino
                st.subheader("Camino Óptimo")
                path = result['path']
                path_str = " → ".join([f"Nodo {node+1}" for node in path])
                st.write(f"**Ruta:** {path_str}")
                
                # Mostrar detalles del camino
                st.subheader("Detalles del Camino")
                if len(path) > 1:
                    total_distance = 0
                    path_details = []
                    
                    for i in range(len(path) - 1):
                        from_node = path[i]
                        to_node = path[i + 1]
                        distance = adjacency_matrix[from_node][to_node]
                        total_distance += distance
                        path_details.append({
                            'Desde': f'Nodo {from_node + 1}',
                            'Hacia': f'Nodo {to_node + 1}',
                            'Distancia': f'{distance:.2f}'
                        })
                    
                    path_df = pd.DataFrame(path_details)
                    st.dataframe(path_df, use_container_width=True)
                    
                    st.metric("Distancia Total Verificada", f"{total_distance:.2f}")
                else:
                    st.info("El nodo de inicio y destino son el mismo.")
                
                # Mostrar todas las distancias desde el nodo de inicio
                st.subheader("Distancias desde el Nodo de Inicio")
                distances = result['all_distances']
                distances_df = pd.DataFrame({
                    'Nodo': [f'Nodo {i+1}' for i in range(num_nodes)],
                    'Distancia': [f"{dist:.2f}" if dist != float('inf') else "∞" for dist in distances]
                })
                st.dataframe(distances_df, use_container_width=True)
                
            else:
                st.error(f"❌ Error al encontrar el camino: {result.get('error', 'Error desconocido')}")
                
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
    
    # Visualización de la red
    with st.expander("📊 Visualización de la Red"):
        st.write("**Representación gráfica de la red:**")
        
        # Crear un diagrama simple usando texto
        nodes = [f"N{i+1}" for i in range(num_nodes)]
        
        # Mostrar conexiones
        connections = []
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j and adjacency_matrix[i][j] > 0:
                    connections.append(f"{nodes[i]} → {nodes[j]} ({adjacency_matrix[i][j]:.1f})")
        
        if connections:
            for conn in connections:
                st.write(f"• {conn}")
        else:
            st.write("No hay conexiones definidas.")
    
    # Información adicional
    with st.expander("ℹ️ Información sobre el Problema de Camino Más Corto"):
        st.markdown("""
        **¿Qué es el Problema de Camino Más Corto?**
        
        Es un problema de optimización en grafos que busca encontrar la ruta de menor costo 
        entre dos nodos en una red.
        
        **Características:**
        - **Grafo dirigido o no dirigido**
        - **Pesos no negativos** en las aristas
        - **Objetivo:** Minimizar la suma de pesos del camino
        
        **Algoritmos comunes:**
        - **Dijkstra:** Para grafos con pesos no negativos
        - **Bellman-Ford:** Para grafos con pesos negativos
        - **Floyd-Warshall:** Para todos los pares de nodos
        - **A\*:** Para búsqueda heurística
        
        **Aplicaciones:**
        - Planificación de rutas (GPS)
        - Redes de comunicación
        - Optimización de redes de transporte
        - Análisis de redes sociales
        - Sistemas de recomendación
        """)
    
    # Ejemplo práctico
    with st.expander("📝 Ejemplo Práctico"):
        st.markdown("""
        **Ejemplo: Red de Ciudades**
        
        Considera una red de ciudades conectadas por carreteras:
        
        ```
        A ----5---- B
        |           |
        3           2
        |           |
        C ----1---- D
        ```
        
        **Distancias:**
        - A → B: 5 km
        - A → C: 3 km  
        - B → D: 2 km
        - C → D: 1 km
        
        **Camino más corto de A a D:**
        - A → C → D: 3 + 1 = 4 km ✓
        - A → B → D: 5 + 2 = 7 km
        
        La ruta óptima es A → C → D con una distancia total de 4 km.
        """)
