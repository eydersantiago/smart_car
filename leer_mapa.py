def leer_mapa(ruta_archivo):
    """
    Lee el archivo de texto que representa la cuadrícula de la ciudad.

    :param ruta_archivo: Ruta al archivo de texto.
    :return: Matriz 10x10 que representa el mapa.
    """
    mapa = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            fila = list(map(int,linea.strip().split()))
            if len(fila) != 10:
                raise ValueError("Cada fila debe tener 10 elementos")
            mapa.append(fila)
    if len(mapa) != 10:
        raise ValueError("El mapa debe tener 10 filas")
    return mapa