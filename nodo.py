class Nodo:
    def __init__(self, ciudad, padre=None, accion=None, prfundida=0):
        self.ciudad = ciudad # Ciudad actual (matriz)
        self.padre = padre # Nodo padre
        self.accion = accion # Acción que generó el nodo
        self.profundidad = prfundida # Profundida en el árbol de búsqueda

    def mover(self, direccion):
        """
        Genera un nuevo estado d ela ciudad moviendo el vehiculo en la dirección indicada

        :param direccion: Dirección en la que se moverá el vehículo (1: Izquierda, 2: Abajo, 3: Derecha, 4: Arriba)

        :returunr: Nueva matriz que representa el estado de la ciudad después del movimiento
        """

        fila, columna = self.econtrar_posicion(2) # Encuentra la posición del vehículo
        hijo = [fila[:] for fila in self.ciudad] # Copia la matriz de la ciudad

        if direccion == 1 and columna > 0:  # Mover a la izquierda
            hijo[fila][columna], hijo[fila][columna-1] = hijo[fila][columna-1], hijo[fila][columna]
        elif direccion == 2 and fila < 9:  # Mover abajo
            hijo[fila][columna], hijo[fila+1][columna] = hijo[fila+1][columna], hijo[fila][columna]
        elif direccion ==3 and fila <9: # Mover a la derecha
            hijo[fila][columna], hijo[fila][columna+1] = hijo[fila][columna+1], hijo[fila][columna]
        elif direccion == 2 and fila > 0:  # Mover arriba
            hijo[fila][columna], hijo[fila-1][columna] = hijo[fila-1][columna], hijo[fila][columna]
        else:
            return None

        return hijo

    def encontrar_posicion(self, valor):
        """
        Encuentra la posición de un valor específico en la cuadrícula.

        :param valor: Valor a buscar.
        :return: Tupla (fila, columna) de la posición encontrada.
        """
        for i in range(10): # Recorre las filas
            for j in range(10): # Recorre las columnas
                if self.ciudad[i][j] == valor: 
                    return i, j
        return -1, -1 # Valor no encontrado

        def meta(self):
            """
            Verifica si el nodo actual es el nodo meta.

            :return: True si el vehículo ha llegado al destino (valor 6), False en caso contrario.
            """

            fila_destino, columna_destino = self.encontrar_posicion(6) # Encuentra la posición del destino
            fila_vehiculo, columna_vehiculo = self.encontrar_posicion(2) # Encuentra la posición del vehículo

            return (fila_destino, columna_destino) == (fila_vehiculo, columna_vehiculo) # Compara las posiciones

        
        def obtener_camino(self):
            """
            Reconstruye el camino desde el nodo inicial hasta este nodo.

            :return: Lista de acciones que llevan al nodo meta.
            """

            camino = []
            nodo = self
            while nodo.padre is not None: # Mientras no se llegue al nodo inicial
                camino.append(nodo.accion) # Agrega la acción al camino
                nodo = nodo.padre # Se mueve al nodo padre
            camino.reverse() # Invierte el camino
            return camino