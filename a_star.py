import heapq

class AStarMixin:
    def busqueda_a_estrella(self):
        print("Iniciando A*: Vehículo -> Pasajero")
        camino1, nodos1, profundidad1, exploracion1, costo1 = self.busqueda_a_estrella_total(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, exploracion1, None  

        print("Iniciando A*: Pasajero -> Destino")
        camino2, nodos2, profundidad2, exploracion2, costo2 = self.busqueda_a_estrella_total(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion1 + exploracion2, None  

        camino_total = camino1 + camino2[1:]

        exploracion_total = exploracion1 + exploracion2

        costo_total = costo1 + costo2

        return camino_total, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion_total, costo_total

    def busqueda_a_estrella_total(self, inicio, objetivo):
        def heuristica(posicion):
            return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])

        cola = [(0 + heuristica(inicio), 0, inicio, [inicio])]
        visitados = set()
        nodos_expandidos = 0
        exploracion = []

        while cola:
            _, costo_actual, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)

            if nodo == objetivo:
                return camino, nodos_expandidos, len(camino) - 1, exploracion, costo_actual
            
            if nodo in visitados:
                continue
            
            visitados.add(nodo)

            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    costo_vecino = costo_actual + self.mapa[vecino[0]][vecino[1]]  
                    heapq.heappush(cola, (costo_vecino + heuristica(vecino), costo_vecino, vecino, camino + [vecino]))

        return None, nodos_expandidos, None, exploracion, None 
