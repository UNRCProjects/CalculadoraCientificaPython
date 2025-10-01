def mcd(a, b):
    """Devuelve el máximo común divisor de dos números"""
    a = int(a)
    b = int(b)
    while b:
        a, b = b, a % b
    return abs(a)

def mcm(a, b):
    """Devuelve el mínimo común múltiplo de dos números"""
    a = int(a)
    b = int(b)
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // mcd(a, b)

def coprimos(a, b):
    """Devuelve True si a y b son primos entre sí (coprimos), False en caso contrario."""
    return mcd(a, b) == 1

def es_primo(n):
    """Devuelve True si n es primo, False en caso contrario."""
    n = int(n)
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
