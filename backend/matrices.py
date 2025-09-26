def suma_matrices(matriz_a, matriz_b):
    """Suma dos matrices del mismo tamaño"""
    if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    resultado = []
    for i in range(len(matriz_a)):
        fila = []
        for j in range(len(matriz_a[0])):
            fila.append(matriz_a[i][j] + matriz_b[i][j])
        resultado.append(fila)
    return resultado

def resta_matrices(matriz_a, matriz_b):
    """Resta dos matrices del mismo tamaño"""
    if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    resultado = []
    for i in range(len(matriz_a)):
        fila = []
        for j in range(len(matriz_a[0])):
            fila.append(matriz_a[i][j] - matriz_b[i][j])
        resultado.append(fila)
    return resultado

def multiplicacion_matrices(matriz_a, matriz_b):
    """Multiplica dos matrices compatibles"""
    if len(matriz_a[0]) != len(matriz_b):
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B")
    
    resultado = []
    for i in range(len(matriz_a)):
        fila = []
        for j in range(len(matriz_b[0])):
            suma = 0
            for k in range(len(matriz_b)):
                suma += matriz_a[i][k] * matriz_b[k][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado

def multiplicacion_escalar(matriz, escalar):
    """Multiplica una matriz por un escalar"""
    resultado = []
    for i in range(len(matriz)):
        fila = []
        for j in range(len(matriz[0])):
            fila.append(matriz[i][j] * escalar)
        resultado.append(fila)
    return resultado

def transpuesta(matriz):
    """Calcula la transpuesta de una matriz"""
    resultado = []
    for j in range(len(matriz[0])):
        fila = []
        for i in range(len(matriz)):
            fila.append(matriz[i][j])
        resultado.append(fila)
    return resultado

def determinante(matriz):
    """Calcula el determinante de una matriz cuadrada usando eliminación gaussiana"""
    n = len(matriz)
    if n != len(matriz[0]):
        raise ValueError("La matriz debe ser cuadrada")
    
    # Crear una copia para no modificar la original
    det_matriz = [fila[:] for fila in matriz]
    det = 1
    
    for i in range(n):
        # Buscar el elemento pivote
        max_row = i
        for k in range(i + 1, n):
            if abs(det_matriz[k][i]) > abs(det_matriz[max_row][i]):
                max_row = k
        
        # Intercambiar filas si es necesario
        if max_row != i:
            det_matriz[i], det_matriz[max_row] = det_matriz[max_row], det_matriz[i]
            det *= -1
        
        # Si el elemento pivote es cero, el determinante es cero
        if det_matriz[i][i] == 0:
            return 0
        
        # Eliminación gaussiana
        for k in range(i + 1, n):
            factor = det_matriz[k][i] / det_matriz[i][i]
            for j in range(i, n):
                det_matriz[k][j] -= factor * det_matriz[i][j]
    
    # Calcular el determinante como producto de los elementos diagonales
    for i in range(n):
        det *= det_matriz[i][i]
    
    return det

def matriz_inversa(matriz):
    """Calcula la matriz inversa usando eliminación gaussiana"""
    n = len(matriz)
    if n != len(matriz[0]):
        raise ValueError("La matriz debe ser cuadrada")
    
    det = determinante(matriz)
    if abs(det) < 1e-10:
        raise ValueError("La matriz es singular (determinante = 0), no tiene inversa")
    
    # Crear matriz aumentada [A|I]
    aumentada = []
    for i in range(n):
        fila = matriz[i][:] + [1 if j == i else 0 for j in range(n)]
        aumentada.append(fila)
    
    # Eliminación gaussiana hacia adelante
    for i in range(n):
        # Buscar el elemento pivote
        max_row = i
        for k in range(i + 1, n):
            if abs(aumentada[k][i]) > abs(aumentada[max_row][i]):
                max_row = k
        
        # Intercambiar filas
        aumentada[i], aumentada[max_row] = aumentada[max_row], aumentada[i]
        
        # Hacer el elemento pivote igual a 1
        pivot = aumentada[i][i]
        for j in range(2 * n):
            aumentada[i][j] /= pivot
        
        # Eliminar elementos debajo del pivote
        for k in range(i + 1, n):
            factor = aumentada[k][i]
            for j in range(2 * n):
                aumentada[k][j] -= factor * aumentada[i][j]
    
    # Eliminación gaussiana hacia atrás
    for i in range(n - 1, -1, -1):
        for k in range(i - 1, -1, -1):
            factor = aumentada[k][i]
            for j in range(2 * n):
                aumentada[k][j] -= factor * aumentada[i][j]
    
    # Extraer la matriz inversa
    inversa = []
    for i in range(n):
        fila = aumentada[i][n:]
        inversa.append(fila)
    
    return inversa

def matriz_identidad(n):
    """Crea una matriz identidad de tamaño n x n"""
    resultado = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(1 if i == j else 0)
        resultado.append(fila)
    return resultado

def traza_matriz(matriz):
    """Calcula la traza de una matriz cuadrada"""
    if len(matriz) != len(matriz[0]):
        raise ValueError("La matriz debe ser cuadrada")
    
    traza = 0
    for i in range(len(matriz)):
        traza += matriz[i][i]
    return traza
