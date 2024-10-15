import heapq

class AStarMixin:
    def busqueda_a_estrella(self):
        """
        Realiza A* desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos y el orden de exploración.
        """
        # Primera A*: Vehículo -> Pasajero
        print("Iniciando A*: Vehículo -> Pasajero")
        camino1, nodos1, profundidad1, exploracion1 = self.busqueda_a_estrella_total(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, exploracion1  # No encontró al pasajero

        # Segunda A*: Pasajero -> Destino
        print("Iniciando A*: Pasajero -> Destino")
        camino2, nodos2, profundidad2, exploracion2 = self.busqueda_a_estrella_total(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion1 + exploracion2  # No encontró el destino

        # Combinar caminos, evitando duplicar el pasajero
        camino_total = camino1 + camino2[1:]

        # Combinar exploraciones
        exploracion_total = exploracion1 + exploracion2

        return camino_total, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion_total

    def busqueda_a_estrella_total(self, inicio, objetivo):
        """
        Algoritmo A*.
        Encuentra el camino más barato desde el inicio hasta el objetivo utilizando una combinación de costo y heurística.
        """
        def heuristica(posicion):
            return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])

        # Cola de prioridad, inicialmente contiene el nodo de inicio
        cola = [(0 + heuristica(inicio), 0, inicio, [inicio])]
        visitados = set()
        nodos_expandidos = 0
        exploracion = []
        
        while cola:
            _, costo, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)
            
            # Si hemos llegado al nodo objetivo, devolvemos el camino, nodos expandidos y el costo
            if nodo == objetivo:
                self.profundidad +=1 
                return camino, nodos_expandidos, self.profundidad, exploracion
            
            if nodo in visitados:
                self.profundidad +=1 
                continue
            visitados.add(nodo)

            # Expandir los vecinos del nodo actual
            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    costo_vecino = costo + 1  # Asignar un costo fijo de 1 para cada movimiento
                    heapq.heappush(cola, (costo_vecino + heuristica(vecino), costo_vecino, vecino, camino + [vecino]))

        # Si no se encuentra un camino, devolvemos None
        return None, nodos_expandidos, self.profundidad, exploracion


