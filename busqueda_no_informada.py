from nodo import Nodo

def busqueda_profundidad_eviar_ciclos(nodo_inicial):
    """
    Realiza una búsqueda en profundidad evitando ciclos para encontrar el nodo meta.

    :param nodo_inicial: Nodo inicial de la búsqueda.
    :return: Nodo meta si se encuentra, None en caso contrario.
    """

    pila = [] # pila para manejar la búsqueda em profundidad
    visitados = set()   # Conjunto para almacenar los nodos visitados

    # Agrega el nodo inicial a la pila
    pila.append(nodo_inicial)

    nodos_expandidos = 0 # Contador de nodos expandidos

    while pila:
        nodo_actual = pila.pop() # Extrae el nodo de la pila
        nodos_expandidos += 1 # Incrementa el contador de nodos expandidos

        #Convertir el estado actual a una representación inmutable para evitar ciclos
        estado = tuple(tuple(fila) for fila in nodo_actual.ciudad)

        #verifica si ya se visitó

        if estado in visitados:
            continue

        # Marca el estado actual como visitado
        visitados.add(estado)

        # Verifica si el nodo actual es el nodo meta
        if nodo_actual.meta():
            print("¡Solución encontrada!")
            print(f"Profundidad: {nodo_actual.profundidad}")
            print(f"Nodos expandidos: {nodos_expandidos}")
            return nodo_actual # Retorna el nodo meta

        # Generar hijos (nuevos movimientos)
        for direccion in range(1,5): # 1: Izquierda, 2: Abajo, 3: Derecha, 4: Arriba
            nuevo_estado = nodo_actual.mover(direccion) # Genera un nuevo estado
            if nuevo_estado is not None:   # Si el movimiento es válido
                hijo = Nodo(
                     ciudad=nuevo_estado,  # Nuevo estado
                     padre=nodo_actual,  # Nodo actual como padre
                     accion=direccion,  # Dirección que generó el estado
                     profundidad=nodo_actual.profundidad + 1) # Incrementa la profundidad
                pila.append(hijo) # Agrega el hijo a la pila

    print("¡No se encontró solución!")
    return None # No se encontró solución


def accion_direccion(direcion):

    """
    Convierte el número de dirección a una descripción textual.

    :param direccion: Número de dirección (1-4).
    :return: Descripción de la dirección.
    """
    return {
        1: "Izquierda",
        2: "Abajo",
        3: "Derecha",
        4: "Arriba"
    }.get(direccion, "Desconocida")
