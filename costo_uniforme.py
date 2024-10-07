import heapq

class CostoUniformeMixin:
    def busqueda_costo_uniforme(self, inicio, objetivo):
        """
        Algoritmo de búsqueda de costo uniforme.
        Encuentra el camino más barato desde el nodo de inicio hasta el nodo objetivo,
        considerando los costos de cada casilla. También registra el orden de expansión de los nodos.
        """
        cola = [(0, inicio, [inicio])]  # (costo acumulado, nodo actual, camino recorrido)
        visitados = set()
        nodos_expandidos = 0
        exploracion = []  # Almacena el orden de exploración de los nodos

        while cola:
            costo, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)
            print(f"Nodo {nodos_expandidos}: {nodo} con costo acumulado {costo}")  # Imprimir nodo visitado

            if nodo == objetivo:
                return camino, nodos_expandidos, costo, exploracion

            if nodo in visitados:
                continue
            visitados.add(nodo)

            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    costo_vecino = costo + self.mapa[vecino[0]][vecino[1]]
                    heapq.heappush(cola, (costo_vecino, vecino, camino + [vecino]))

        return None, nodos_expandidos, float('inf'), exploracion  # Si no se encuentra un camino

    def busqueda_costo_uniforme_total(self):
        """
        Realiza búsqueda de costo uniforme desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos, el costo total y el orden de exploración.
        """
        # Primera búsqueda: Vehículo -> Pasajero
        print("Iniciando búsqueda de costo uniforme: Vehículo -> Pasajero")
        camino1, nodos1, costo1, exploracion1 = self.busqueda_costo_uniforme(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, float('inf'), exploracion1  # No encontró al pasajero

        # Segunda búsqueda: Pasajero -> Destino
        print("Iniciando búsqueda de costo uniforme: Pasajero -> Destino")
        camino2, nodos2, costo2, exploracion2 = self.busqueda_costo_uniforme(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, float('inf'), exploracion1 + exploracion2  # No encontró el destino

        # Combinar caminos, evitando duplicar el pasajero
        camino_total = camino1 + camino2[1:]

        # Sumar costos
        costo_total = costo1 + costo2

        # Combinar exploraciones
        exploracion_total = exploracion1 + exploracion2

        return camino_total, nodos1 + nodos2, costo_total, exploracion_total
