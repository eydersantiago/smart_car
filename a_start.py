import heapq

class AStarMixin:
    def busqueda_a_estrella(self):
        print("Iniciando A*: Vehículo -> Pasajero")

        camino1, nodos1, profundidad1, exploracion1, costo1 = self.busqueda_a_estrella_total(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, exploracion1, None  # No encontró al pasajero

        print("Iniciando A*: Pasajero -> Destino")

        camino2, nodos2, profundidad2, exploracion2, costo2 = self.busqueda_a_estrella_total(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion1 + exploracion2, None  # No encontró el destino

        # Combinar caminos
        camino_total = camino1 + camino2[1:]

        # Combinar exploraciones
        exploracion_total = exploracion1 + exploracion2

        # Sumar costos
        costo_total = costo1 + costo2

        return camino_total, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion_total, costo_total

    def busqueda_a_estrella_total(self, inicio, objetivo):
        def heuristica(posicion):
            # Asegúrate de que esta heurística sea apropiada para tu problema
            return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])

        cola = [(0 + heuristica(inicio), 0, inicio, [inicio])]
        visitados = set()
        nodos_expandidos = 0
        exploracion = []

        # Inicializar profundidad
        self.profundidad = 0

        while cola:
            _, costo_actual, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)

            # Incrementar profundidad cada vez que se expande un nodo
            self.profundidad = len(camino) - 1  # Profundidad es el tamaño del camino menos 1

            if nodo == objetivo:
                return camino, nodos_expandidos, self.profundidad, exploracion, costo_actual
            
            if nodo in visitados:
                continue
            
            visitados.add(nodo)

            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    costo_vecino = costo_actual + 1  # Asegúrate de que este costo sea correcto
                    heapq.heappush(cola, (costo_vecino + heuristica(vecino), costo_vecino, vecino, camino + [vecino]))

        return None, nodos_expandidos, self.profundidad, exploracion, None
