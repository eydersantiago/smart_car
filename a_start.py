import heapq

class AStarMixin:
    def busqueda_a_estrella(self):
        """
        Realiza A* desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos, el orden de exploración, y el costo total.
        """
        # Primera A*: Vehículo -> Pasajero
        print("Iniciando A*: Vehículo -> Pasajero")
        camino1, nodos1, exploracion1, costo1 = self.busqueda_a_estrella_total(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, exploracion1, None  # No encontró al pasajero

        # Segunda A*: Pasajero -> Destino
        print("Iniciando A*: Pasajero -> Destino")
        camino2, nodos2, exploracion2, costo2 = self.busqueda_a_estrella_total(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, exploracion1 + exploracion2, None  # No encontró el destino

        # Combinar caminos, evitando duplicar el pasajero
        camino_total = camino1 + camino2[1:]

        # Combinar exploraciones
        exploracion_total = exploracion1 + exploracion2

        # Sumar los costos de ambos trayectos
        costo_total = costo1 + costo2

        return camino_total, nodos1 + nodos2, exploracion_total, costo_total

    def busqueda_a_estrella_total(self, inicio, objetivo):
        """
        Algoritmo A*.
        Encuentra el camino más barato desde el inicio hasta el objetivo utilizando una combinación de costo y heurística.
        También retorna el costo total del camino encontrado.
        """
        def heuristica(posicion):
            return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])

        # Cola de prioridad, inicialmente contiene el nodo de inicio
        cola = [(0 + heuristica(inicio), 0, inicio, [inicio])]  # (costo_total, costo_real, nodo, camino)
        visitados = set()
        nodos_expandidos = 0
        exploracion = []
        
        while cola:
            _, costo_real, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)
            
            # Si hemos llegado al nodo objetivo, devolvemos el camino, nodos expandidos, exploración y el costo real
            if nodo == objetivo:
                return camino, nodos_expandidos, exploracion, costo_real
            
            if nodo in visitados:
                continue
            visitados.add(nodo)

            # Expandir los vecinos del nodo actual
            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    costo_vecino = costo_real + 1  # Asignar un costo fijo de 1 para cada movimiento
                    heapq.heappush(cola, (costo_vecino + heuristica(vecino), costo_vecino, vecino, camino + [vecino]))

        # Si no se encuentra un camino, devolvemos None
        return None, nodos_expandidos, exploracion, None
