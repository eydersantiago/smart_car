class DFSMixin:
    def busqueda_profundidad(self, inicio, objetivo):
        """
        Algoritmo de búsqueda en profundidad (DFS).
        Encuentra un camino desde el nodo de inicio hasta el nodo objetivo sin considerar costos.
        Además, registra el orden de expansión de los nodos para visualización.
        """
        pila = [inicio]  # Usamos una pila (LIFO) en lugar de una cola para la búsqueda en profundidad
        visitados = set([inicio])  # Mantener un conjunto de nodos visitados
        padres = {}  # Almacena los predecesores para reconstruir el camino
        exploracion = []  # Almacena el orden de exploración de los nodos
        contador_nodos = 0  # Contador de nodos expandidos local

        while pila:
            actual = pila.pop()
            exploracion.append(actual)
            contador_nodos += 1
            print(f"Nodo {contador_nodos}: {actual}")  # Imprimir nodo visitado

            if actual == objetivo:
                # Reconstruir el camino desde el objetivo hasta el inicio
                camino = []
                while actual in padres:
                    camino.append(actual)
                    actual = padres[actual]
                    self.profundidad +=1 
                camino.append(inicio)
                camino.reverse()
                return camino, contador_nodos, self.profundidad, exploracion

            # Expandir los nodos vecinos no visitados
            for vecino in self.vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    pila.append(vecino)

        return None, contador_nodos, self.profundidad, exploracion  # Si no encuentra el objetivo

    def busqueda_profundidad_total(self):
        """
        Realiza DFS desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos y el orden de exploración.
        """
        # Primera DFS: Vehículo -> Pasajero
        print("Iniciando DFS: Vehículo -> Pasajero")
        camino1, nodos1, profundidad1, exploracion1 = self.busqueda_profundidad(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, exploracion1  # No encontró al pasajero

        # Segunda DFS: Pasajero -> Destino
        print("Iniciando DFS: Pasajero -> Destino")
        camino2, nodos2, profundidad2, exploracion2 = self.busqueda_profundidad(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion1 + exploracion2  # No encontró el destino

        # Combinar caminos, evitando duplicar el pasajero
        camino_total = camino1 + camino2[1:]

        # Combinar exploraciones
        exploracion_total = exploracion1 + exploracion2

        return camino_total, nodos1 + nodos2, self.profundidad, exploracion_total
