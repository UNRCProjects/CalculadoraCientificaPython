def multiplicar_matrices(matriz_a, matriz_b):
    """Multiplica dos matrices 2x2 y devuelve el resultado."""
    # Para matrices 2x2 específicamente
    resultado = [[0, 0], [0, 0]]
    
    resultado[0][0] = matriz_a[0][0] * matriz_b[0][0] + matriz_a[0][1] * matriz_b[1][0]
    resultado[0][1] = matriz_a[0][0] * matriz_b[0][1] + matriz_a[0][1] * matriz_b[1][1]
    resultado[1][0] = matriz_a[1][0] * matriz_b[0][0] + matriz_a[1][1] * matriz_b[1][0]
    resultado[1][1] = matriz_a[1][0] * matriz_b[0][1] + matriz_a[1][1] * matriz_b[1][1]
    
    return resultado
