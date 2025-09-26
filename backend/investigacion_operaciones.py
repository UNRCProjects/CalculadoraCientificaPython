import numpy as np
from scipy.optimize import linprog

def transportation_problem(cost_matrix, supply, demand):
    """
    Resuelve el problema de transporte usando el método simplex.
    
    Args:
        cost_matrix (list): Matriz de costos [origen][destino]
        supply (list): Ofertas de cada origen
        demand (list): Demandas de cada destino
        
    Returns:
        dict: Solución del problema de transporte
    """
    try:
        origins = len(supply)
        destinations = len(demand)
        
        # Verificar balance
        total_supply = sum(supply)
        total_demand = sum(demand)
        
        if total_supply != total_demand:
            return {
                'success': False,
                'error': f'Problema no balanceado: Oferta={total_supply}, Demanda={total_demand}',
                'solution': None
            }
        
        # Convertir a problema de programación lineal
        # Variables: x[i][j] = cantidad transportada de origen i a destino j
        num_vars = origins * destinations
        
        # Función objetivo: minimizar costos
        c = []
        for i in range(origins):
            for j in range(destinations):
                c.append(cost_matrix[i][j])
        
        # Restricciones de oferta (suma por fila = supply[i])
        A_eq = []
        b_eq = []
        
        for i in range(origins):
            constraint = [0] * num_vars
            for j in range(destinations):
                constraint[i * destinations + j] = 1
            A_eq.append(constraint)
            b_eq.append(supply[i])
        
        # Restricciones de demanda (suma por columna = demand[j])
        for j in range(destinations):
            constraint = [0] * num_vars
            for i in range(origins):
                constraint[i * destinations + j] = 1
            A_eq.append(constraint)
            b_eq.append(demand[j])
        
        # Límites: x >= 0
        bounds = [(0, None)] * num_vars
        
        # Resolver usando scipy
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if result.success:
            # Reconstruir matriz de solución
            solution_matrix = []
            for i in range(origins):
                row = []
                for j in range(destinations):
                    idx = i * destinations + j
                    row.append(result.x[idx])
                solution_matrix.append(row)
            
            return {
                'success': True,
                'solution_matrix': solution_matrix,
                'total_cost': result.fun,
                'status': result.message
            }
        else:
            return {
                'success': False,
                'error': result.message,
                'solution': None
            }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'solution': None
        }

def shortest_path(adjacency_matrix, start, end):
    """
    Encuentra el camino más corto usando el algoritmo de Dijkstra.
    
    Args:
        adjacency_matrix (list): Matriz de adyacencia con distancias
        start (int): Nodo de inicio
        end (int): Nodo de destino
        
    Returns:
        dict: Solución del problema de camino más corto
    """
    try:
        n = len(adjacency_matrix)
        
        # Verificar nodos válidos
        if start < 0 or start >= n or end < 0 or end >= n:
            return {
                'success': False,
                'error': 'Nodos de inicio o destino inválidos',
                'path': None,
                'distance': None
            }
        
        # Inicializar distancias
        distances = [float('inf')] * n
        distances[start] = 0
        previous = [-1] * n
        visited = [False] * n
        
        # Algoritmo de Dijkstra
        for _ in range(n):
            # Encontrar nodo no visitado con menor distancia
            min_dist = float('inf')
            current = -1
            
            for i in range(n):
                if not visited[i] and distances[i] < min_dist:
                    min_dist = distances[i]
                    current = i
            
            if current == -1:
                break
            
            visited[current] = True
            
            # Actualizar distancias de nodos adyacentes
            for neighbor in range(n):
                if (not visited[neighbor] and 
                    adjacency_matrix[current][neighbor] > 0 and 
                    distances[current] + adjacency_matrix[current][neighbor] < distances[neighbor]):
                    
                    distances[neighbor] = distances[current] + adjacency_matrix[current][neighbor]
                    previous[neighbor] = current
        
        # Reconstruir camino
        if distances[end] == float('inf'):
            return {
                'success': False,
                'error': 'No existe camino entre los nodos',
                'path': None,
                'distance': None
            }
        
        path = []
        current = end
        while current != -1:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return {
            'success': True,
            'path': path,
            'distance': distances[end],
            'all_distances': distances
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'path': None,
            'distance': None
        }