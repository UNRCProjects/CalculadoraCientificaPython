# Importamos la librería 'math' para poder hacer operaciones como la raíz cuadrada.
import math

def sumar(a, b):
    # Esta función simplemente devuelve la suma de dos números.
    return a + b

def restar(a, b):
    # Esta función devuelve la resta de dos números.
    return a - b

def multiplicar(a, b):
    # Esta función devuelve la multiplicación de dos números.
    return a * b

def dividir(a, b):
    # Para la división, primero revisamos si el segundo número es cero.
    if b == 0:
        # Si es cero, no se puede dividir, así que mandamos un mensaje de error.
        return "Error: División por cero"
    return a / b

def raiz_cuadrada(a):
    # Para la raíz cuadrada, revisamos que el número no sea negativo.
    if a < 0:
        # Si es negativo, mandamos un error.
        return "Error: No se puede calcular la raíz de un número negativo"
    return math.sqrt(a)
