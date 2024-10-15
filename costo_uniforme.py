import heapq

class CostoUniformeMixin:
    def busqueda_costo_uniforme(self, inicio, objetivo):
        """
        Algoritmo de búsqueda de costo uniforme.
        Encuentra el camino más barato desde el nodo de inicio hasta el nodo objetivo,
        considerando los costos de cada casilla. También registra el orden de expansión de los nodos.
        """
        cola = [(0, inicio, [inicio])]  
        visitados = set()
        nodos_expandidos = 0
        self.profundidad = 0
        exploracion = []  

        while cola:
            costo, nodo, camino = heapq.heappop(cola)
            nodos_expandidos += 1
            exploracion.append(nodo)
            print(f"Nodo {nodos_expandidos}: {nodo} con costo acumulado {costo}") 
            
            if nodo == objetivo:
                self.profundidad +=1
                return camino, nodos_expandidos, self.profundidad, costo, exploracion

            if nodo in visitados:
                self.profundidad +=1 
                continue
                
            visitados.add(nodo)
                
            for vecino in self.vecinos(nodo):
                if vecino not in visitados:
                    costo_vecino = costo + self.mapa[vecino[0]][vecino[1]]
                    heapq.heappush(cola, (costo_vecino, vecino, camino + [vecino]))

        return None, nodos_expandidos, self.profundidad, float('inf'), exploracion 

    def busqueda_costo_uniforme_total(self):
        """
        Realiza búsqueda de costo uniforme desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos, el costo total y el orden de exploración.
        """
        print("Iniciando búsqueda de costo uniforme: Vehículo -> Pasajero")
        camino1, nodos1, profundidad1, costo1, exploracion1 = self.busqueda_costo_uniforme(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, float('inf'), exploracion1  #

        print("Iniciando búsqueda de costo uniforme: Pasajero -> Destino")
        camino2, nodos2, profundidad2, costo2, exploracion2 = self.busqueda_costo_uniforme(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2),float('inf'), exploracion1 + exploracion2  

        camino_total = camino1 + camino2[1:]

        costo_total = costo1 + costo2


        exploracion_total = exploracion1 + exploracion2

        return camino_total, nodos1 + nodos2, max(profundidad1, profundidad2), costo_total, exploracion_total
