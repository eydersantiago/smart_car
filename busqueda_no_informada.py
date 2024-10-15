class DFSMixin:
    def busqueda_profundidad(self, inicio, objetivo):
        """
        Algoritmo de búsqueda en profundidad (DFS).
        Encuentra un camino desde el nodo de inicio hasta el nodo objetivo sin considerar costos.
        Además, registra el orden de expansión de los nodos para visualización.
        """
        pila = [inicio]  
        visitados = set([inicio])  
        padres = {}  
        exploracion = []  
        contador_nodos = 0
        self.profundidad = 0 

        while pila:
            actual = pila.pop()
            exploracion.append(actual)
            contador_nodos += 1
            print(f"Nodo {contador_nodos}: {actual}")  

            if actual == objetivo:

                camino = []
                while actual in padres:
                    camino.append(actual)
                    actual = padres[actual]
                    self.profundidad +=1 
                camino.append(inicio)
                camino.reverse()
                return camino, contador_nodos, self.profundidad, exploracion

            for vecino in self.vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    pila.append(vecino)

        return None, contador_nodos, self.profundidad, exploracion  #

    def busqueda_profundidad_total(self):
        """
        Realiza DFS desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos y el orden de exploración.
        """
        print("Iniciando DFS: Vehículo -> Pasajero")
        camino1, nodos1, profundidad1, exploracion1 = self.busqueda_profundidad(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, profundidad1, exploracion1  

        print("Iniciando DFS: Pasajero -> Destino")
        camino2, nodos2, profundidad2, exploracion2 = self.busqueda_profundidad(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, max(profundidad1, profundidad2), exploracion1 + exploracion2 

        camino_total = camino1 + camino2[1:]

        exploracion_total = exploracion1 + exploracion2

        return camino_total, nodos1 + nodos2, self.profundidad, exploracion_total
