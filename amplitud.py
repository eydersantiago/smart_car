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
        cola = deque() # Cola  para guardar los nodos que se van a explorar
        cola.append(inicio) 
        
        visitados = set() # Conjunto para guardar los nodos visitados y evitar ciclos
        visitados.add(inicio) 
        
        padres = {} # Diccionario para almacenar los padres de cada nodo para reconstruir el camino
        exploracion = [] # Lista para almacenar el orden de exploración de los nodos
        

        # Mientras haya nodos en la cola, se continua explorando
        while cola:
            actual = cola.popleft() # Extrae el primer nodo de la cola
            exploracion.append(actual) # Añade el nodo actual a la lista de exploración
            self.contador_nodos += 1  # Incrementamos el contador de nodos expandidos
            #self.contador_nodos += 1  
            print(f"Nodo {self.contador_nodos}: {actual}")  # Imprimimos el nodo visitado
            
            # Si hemos alcanzado el nodo objetivo, reconstruimos el camino desde el objetivo al inicio
            if actual == objetivo:
                camino = []
                
                # Seguimos los padres para reconstruir el camino
                while actual in padres:
                    camino.append(actual) 
                    actual = padres[actual]
                camino.append(inicio) # Añadimos el nodo de inicio al final
                camino.reverse() # Invertimos el camino para que vaya de inicio a objetivo
                return camino, len(visitados), exploracion # Devolvemos el camino y los resultado

            # Recorremos los vecinos  del nodo actual
            for vecino in self.vecinos(actual):
                # Si el vecino no ha sido visitado, lo añadimos a la cola para explorarlo
                if vecino not in visitados: 
                    visitados.add(vecino) # Marcamos el vecino como visitado
                    padres[vecino] = actual # Registramos el nodo actual como padre del vecino
                    cola.append(vecino) # Añadimos el vecino a la cola para explorar

        return None, len(visitados), exploracion  # Si no encuentra el objetivo, devuelve None y los resultados de la búsqueda


    def busqueda_amplitud_total(self):
        """
        Realiza BFS desde el vehículo al pasajero y luego del pasajero al destino.
        Retorna el camino completo, el total de nodos expandidos y el orden de exploración.
        """
        
        # Primera búsqueda: Vehículo -> Pasajero
        print("Iniciando BFS: Vehículo -> Pasajero")
        camino1, nodos1, exploracion1 = self.busqueda_amplitud(self.posicion_vehiculo, self.posicion_pasajero)
        if not camino1: # Si no se encuentra el pasajero, finaliza la búsqueda y devuelve los resultados hasta el momento
            return None, nodos1, exploracion1  


        # Segunda búsqueda: Pasajero -> Destino
        print("Iniciando BFS: Pasajero -> Destino")
        camino2, nodos2, exploracion2 = self.busqueda_amplitud(self.posicion_pasajero, self.destino)
        if not camino2: # Si no se encuentra el destino, finaliza la búsqueda y devuelve los resultados hasta el momento
            return None, nodos1 + nodos2, exploracion1 + exploracion2  # No encontró el destino
        

        # Combinamos los caminos de las dos búsquedas, evitando duplicar el pasajero
        camino_total = camino1 + camino2[1:]

        # Combinamos las exploraciones de ambas búsquedas
        exploracion_total = exploracion1 + exploracion2

        # Devolvemos el camino completo, el número total de nodos expandidos y el orden de exploración
        return camino_total, self.contador_nodos, exploracion_total
