# amplitud.py

from collections import deque

class BFSMixin:
    def busqueda_amplitud(self, inicio, objetivo):
        """
        Algoritmo de búsqueda en amplitud (BFS).
        Encuentra el camino más corto desde el inicio hasta el objetivo sin considerar costos.
        Además, registra el orden de expansión de los nodos para visualización.
        Imprime en consola cada nodo visitado con su número de orden y coordenadas.
        """
        cola = deque()
        cola.append(inicio)
        visitados = set()
        visitados.add(inicio)
        padres = {}
        exploracion = []  # Orden de exploración

        while cola:
            actual = cola.popleft()
            exploracion.append(actual)
            self.contador_nodos += 1  # Incrementar el contador
            print(f"Nodo {self.contador_nodos}: {actual}")  # Imprimir nodo visitado

            if actual == objetivo:
                # Reconstruir el camino desde el objetivo hasta el inicio
                camino = []
                while actual in padres:
                    camino.append(actual)
                    actual = padres[actual]
                camino.append(inicio)
                camino.reverse()
                return camino, len(visitados), exploracion

            for vecino in self.vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    cola.append(vecino)

        return None, len(visitados), exploracion  # Si no encuentra el objetivo

    def busqueda_amplitud_total(self):
        """
        Realiza BFS desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos y el orden de exploración.
        """
        # Primera BFS: Vehículo -> Pasajero
        print("Iniciando BFS: Vehículo -> Pasajero")
        camino1, nodos1, exploracion1 = self.busqueda_amplitud(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1:
            return None, nodos1, exploracion1  # No encontró al pasajero

        # Segunda BFS: Pasajero -> Destino
        print("Iniciando BFS: Pasajero -> Destino")
        camino2, nodos2, exploracion2 = self.busqueda_amplitud(self.posicion_pasajero, self.destino)
        if not camino2:
            return None, nodos1 + nodos2, exploracion1 + exploracion2  # No encontró el destino

        # Combinar caminos, evitando duplicar el pasajero
        camino_total = camino1 + camino2[1:]

        # Combinar exploraciones
        exploracion_total = exploracion1 + exploracion2

        return camino_total, self.contador_nodos, exploracion_total
