def cifrado_cesar(texto, desplazamiento, modo='cifrar'):
    """
    Cifra o descifra un texto usando el Cifrado César.

    Args:
        texto (str): El texto a procesar.
        desplazamiento (int): El número de posiciones a desplazar.
        modo (str): 'cifrar' para encriptar, 'descifrar' para desencriptar.

    Returns:
        str: El texto procesado.
    """
    if modo == 'descifrar':
        desplazamiento = -desplazamiento

    resultado = ""
    for char in texto:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            codigo_nuevo = (ord(char) - offset + desplazamiento) % 26 + offset
            resultado += chr(codigo_nuevo)
        else:
            resultado += char
    return resultado