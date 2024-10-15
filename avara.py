import heapq

class AvaraMixin:
    def busqueda_avara(self, inicio, objetivo):
        """
        Algoritmo de búsqueda avara (Greedy Search).
        Encuentra el camino desde el nodo de inicio hasta el nodo objetivo utilizando una heurística,
        en este caso, la distancia de Manhattan. Registra también el número de nodos expandidos.
        """
        def heuristica(posicion):
            return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])

        cola = [(heuristica(inicio), inicio, [inicio])]  
        visitados = set()
        nodos_expandidos = 0
        exploracion = [] 

        while cola:
            _, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)
            print(f"Nodo {nodos_expandidos}: {nodo} con heuristica {heuristica(nodo)}") 

            if nodo == objetivo:
                return camino, nodos_expandidos, self.profundidad, exploracion  

            if nodo in visitados:        
                continue
            visitados.add(nodo)
            self.profundidad +=1 
            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    heapq.heappush(cola, (heuristica(vecino), vecino, camino + [vecino]))

        return None, nodos_expandidos, self.profundidad, exploracion  

    def busqueda_avara_total(self):
        """
        Realiza la búsqueda avara desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos y el orden de exploración.
        """

        print("Iniciando búsqueda avara: Vehículo -> Pasajero")
        camino1, nodos1, profundidad1, exploracion1 = self.busqueda_avara(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, exploracion1 

        print("Iniciando búsqueda avara: Pasajero -> Destino")
        camino2, nodos2, profundidad2, exploracion2 = self.busqueda_avara(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion1 + exploracion2  

        camino_total = camino1 + camino2[1:]

        exploracion_total = exploracion1 + exploracion2

        return camino_total, nodos1 + nodos2, self.profundidad, exploracion_total
