import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class CiudadInteligente:
    def __init__(self, archivo_mapa):
        self.mapa = self.cargar_mapa(archivo_mapa)
        self.posicion_vehiculo = self.encontrar_posicion(2)
        self.posicion_pasajero = self.encontrar_posicion(5)
        self.destino = self.encontrar_posicion(6)
    
    def cargar_mapa(self, archivo_mapa):
        """
        Carga el mapa desde un archivo de texto.
        Cada línea del archivo representa una fila del mapa.
        """
        with open(archivo_mapa, 'r') as file:
            return [list(map(int, line.split())) for line in file]

    def encontrar_posicion(self, valor):
        """
        Encuentra la posición (fila, columna) del valor dado en el mapa.
        """
        for i, fila in enumerate(self.mapa):
            if valor in fila:
                return (i, fila.index(valor))

    def vecinos(self, posicion):
        """
        Devuelve los vecinos válidos de una posición dada (movimiento arriba, abajo, izquierda, derecha).
        """
        fila, columna = posicion
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        resultado = []
        for d in direcciones:
            nueva_fila, nueva_columna = fila + d[0], columna + d[1]
            if 0 <= nueva_fila < len(self.mapa) and 0 <= nueva_columna < len(self.mapa[0]):
                if self.mapa[nueva_fila][nueva_columna] != 1:  # No es un muro
                    resultado.append((nueva_fila, nueva_columna))
        return resultado
    
    def busqueda_amplitud(self, inicio, objetivo):
        """
        Algoritmo de búsqueda en amplitud.
        Encuentra el camino más corto desde el inicio hasta el objetivo sin tener en cuenta los costos.
        """
        return 1

    def busqueda_costo_uniforme(self, inicio, objetivo):
        """
        Algoritmo de búsqueda de costo uniforme.
        Encuentra el camino más barato desde el inicio hasta el objetivo, considerando los costos de cada casilla.
        """
        return 1

    def busqueda_profundidad(self, inicio, objetivo):
        """
        Algoritmo de búsqueda en profundidad evitando ciclos.
        Encuentra el camino desde el inicio hasta el objetivo sin tener en cuenta los costos.
        """
        return 1

    def busqueda_avaricia(self, inicio, objetivo):
        """
        Algoritmo de búsqueda avara.
        Encuentra el camino desde el inicio hasta el objetivo utilizando la heurística de distancia Manhattan.
        """
        return 1

    def busqueda_a_estrella(self, inicio, objetivo):
        """
        Algoritmo A*.
        Encuentra el camino más barato desde el inicio hasta el objetivo utilizando una combinación de costo y heurística.
        """
        return 1

class InterfazCiudad:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ciudad Inteligente")
        self.ventana.geometry('900x750')
        self.ventana.configure(bg='#dad082')
        self.crear_frames()
        self.crear_cuadricula()
        self.crear_widgets()
        self.archivo_mapa = None
        self.ciudad = None
        self.ventana.mainloop()

    def crear_frames(self):
        self.content_frame = tk.Frame(self.ventana, bg='#dad082')
        self.content_frame.pack(fill='both', expand=True) 
        self.frame_cuadricula = tk.Frame(self.content_frame, bg='#dad082')
        self.frame_cuadricula.pack(pady=20)
        self.frame_botones = tk.Frame(self.content_frame, bg='#6f96b4')
        self.frame_botones.pack(side=tk.BOTTOM, fill='x')
        self.frame_botones.pack_propagate(False)
        self.frame_botones.configure(height=100)

    def crear_cuadricula(self):
        self.tam_celda = 60
        self.ancho_mapa = self.tam_celda * 10  
        self.alto_mapa = self.tam_celda * 10  
        self.canvas = tk.Canvas(
            self.frame_cuadricula, width=self.ancho_mapa, height=self.alto_mapa, bg='white'
        )
        self.canvas.pack()

    def crear_widgets(self):
        fuente_fresca = ('Comic Sans MS', 12)


        frame_menus = tk.Frame(self.frame_botones, bg='#6f96b4')
        frame_menus.pack(side=tk.LEFT, padx=20, pady=20)
        frame_tipo_busqueda = tk.Frame(frame_menus, bg='#6f96b4')
        frame_tipo_busqueda.pack(side=tk.LEFT, padx=20)

        self.label_tipo_busqueda = tk.Label(
            frame_tipo_busqueda,
            text="Seleccione tipo de búsqueda:",
            bg='#6f96b4',
            font=fuente_fresca
        )
        self.label_tipo_busqueda.pack()
        self.tipo_busqueda = tk.StringVar(value="seleccione")
        self.menu_busqueda = ttk.Combobox(
            frame_tipo_busqueda,
            textvariable=self.tipo_busqueda,
            values=["No informada", "Informada"],
            state="readonly"
        )
        self.menu_busqueda.pack()
        self.menu_busqueda.bind("<<ComboboxSelected>>", self.actualizar_algoritmos)

        self.menu_busqueda.pack()
        frame_algoritmo = tk.Frame(frame_menus, bg='#6f96b4')
        frame_algoritmo.pack(side=tk.LEFT, padx=20)

        self.label_algoritmo = tk.Label(
            frame_algoritmo,
            text="Seleccione algoritmo:",
            bg='#6f96b4',
            font=fuente_fresca
        )
        self.label_algoritmo.pack()
        self.algoritmo = tk.StringVar(value="seleccione")
        self.menu_algoritmo = ttk.Combobox(
            frame_algoritmo,
            textvariable=self.algoritmo,
            state="readonly"
        )
        self.menu_algoritmo.pack()

        frame_accion = tk.Frame(self.frame_botones, bg='#6f96b4')
        frame_accion.pack(side=tk.RIGHT, padx=20, pady=20)

    #Botones
        self.boton_cargar = tk.Button(
            frame_accion,
            text="Cargar Archivo",
            font=fuente_fresca,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            width=15,
            command=self.cargar_archivo
        )
        self.boton_cargar.pack(side=tk.LEFT, padx=5)

        self.boton_buscar = tk.Button(
            frame_accion,
            text="Buscar y Llevar",
            font=fuente_fresca,
            bg='#008CBA',
            fg='white',
            activebackground='#007bb5',
            width=15,
            command=self.ejecutar_busqueda
        )
        self.boton_buscar.pack(side=tk.LEFT, padx=5)

        self.mensaje_estado = tk.Label(
            self.content_frame,
            text="",
            font=fuente_fresca,
            bg='#dad082'
        )
        self.mensaje_estado.pack(side=tk.BOTTOM, fill='x')

    def actualizar_algoritmos(self, event):
        tipo_busqueda = self.tipo_busqueda.get()
        if tipo_busqueda == "No informada":
            opciones = ["Amplitud", "Costo uniforme", "Profundidad evitando ciclos"]
        elif tipo_busqueda == "Informada":
            opciones = ["Avara", "A*"]
        else:
            opciones = []

        self.menu_algoritmo.config(values=opciones)
        self.menu_algoritmo.set(opciones[0] if opciones else "")
        self.menu_algoritmo.config(state=tk.NORMAL if opciones else tk.DISABLED)
        

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            self.archivo_mapa = archivo
            self.ciudad = CiudadInteligente(archivo)
            self.dibujar_mapa()
            self.menu_algoritmo.config(state=tk.NORMAL)
            self.boton_buscar.config(state=tk.NORMAL)

    def dibujar_mapa(self):
        # Dibuja el mapa en el canvas usando colores para diferentes valores
        self.canvas.delete("all")
        self.rectangulos = []
        for i, fila in enumerate(self.ciudad.mapa):
            fila_rectangulos = []
            for j, valor in enumerate(fila):
                x1, y1 = j * self.tam_celda, i * self.tam_celda
                x2, y2 = x1 + self.tam_celda, y1 + self.tam_celda
                # Asigna un color basado en el valor del mapa
                color = 'white' if valor == 0 else 'grey' if valor == 1 else 'yellow' if valor == 2 else '#98FB98' if valor == 3 else 'red' if valor == 4 else 'green' if valor == 5 else 'pink' if valor == 6 else 'white'
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                fila_rectangulos.append(rect)
            self.rectangulos.append(fila_rectangulos)

    def ejecutar_busqueda(self):
        if not self.ciudad:
            messagebox.showerror("Error", "No se ha cargado ningún mapa.")
            return

        tipo_busqueda = self.tipo_busqueda.get()
        algoritmo = self.algoritmo.get()
        inicio = self.ciudad.posicion_vehiculo
        objetivo = self.ciudad.destino

        if tipo_busqueda == "No informada":
            if algoritmo == "Amplitud":
                camino, nodos_expandidos = self.ciudad.busqueda_amplitud(inicio, objetivo)
            elif algoritmo == "Costo uniforme":
                camino, nodos_expandidos, costo = self.ciudad.busqueda_costo_uniforme(inicio, objetivo)
            elif algoritmo == "Profundidad evitando ciclos":
                camino, nodos_expandidos = self.ciudad.busqueda_profundidad(inicio, objetivo)
        elif tipo_busqueda == "Informada":
            if algoritmo == "Avara":
                camino, nodos_expandidos = self.ciudad.busqueda_avaricia(inicio, objetivo)
            elif algoritmo == "A*":
                camino, nodos_expandidos, costo = self.ciudad.busqueda_a_estrella(inicio, objetivo)

        self.dibujar_mapa()
        self.dibujar_camino(camino)

        mensaje = f"Algoritmo: {algoritmo}\nNodos expandidos: {nodos_expandidos}"
        self.mensaje_estado.config(text=mensaje)

    def dibujar_camino(self, camino):
        if camino:
            for (fila, columna) in camino:
                self.canvas.create_rectangle(columna * self.tam_celda, fila * self.tam_celda,
                                             (columna + 1) * self.tam_celda, (fila + 1) * self.tam_celda,
                                             fill="yellow", outline="grey")


if __name__ == "__main__":
    InterfazCiudad()
