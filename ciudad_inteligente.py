import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from amplitud import BFSMixin 
from busqueda_no_informada import DFSMixin 
from costo_uniforme import CostoUniformeMixin
from avara import AvaraMixin


class CiudadInteligente(BFSMixin, DFSMixin, CostoUniformeMixin, AvaraMixin):
    def __init__(self, archivo_mapa):
        self.mapa = self.cargar_mapa(archivo_mapa)
        self.posicion_vehiculo = self.encontrar_posicion(2)
        self.posicion_pasajero = self.encontrar_posicion(5)
        self.destino = self.encontrar_posicion(6)
        self.contador_nodos = 0  # Inicializar el contador de nodos

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
        return None

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

class InterfazCiudadGUI:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ciudad Inteligente")
        self.ventana.geometry('900x700')
        self.ventana.configure(bg='#dad082')
        self.crear_frames()
        self.crear_cuadricula()
        self.crear_widgets()
        self.archivo_mapa = None
        self.ciudad = None
        self.imagen_auto = None  # Para mantener la referencia de PhotoImage
        self.imagen_auto_id = None  # ID del objeto de la imagen en el Canvas
        self.imagen_persona = None  # Para la imagen del pasajero
        self.imagen_persona_id = None  # ID del objeto de la imagen del pasajero
        self.imagen_ubicacion = None  # Para la imagen del destino
        self.imagen_ubicacion_id = None  # ID del objeto de la imagen del destino
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
        self.tam_celda = 50
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
            values=["Búsqueda no informada - evitando ciclos"],
            state="readonly"
        )
        self.menu_algoritmo.pack()

        frame_accion = tk.Frame(self.frame_botones, bg='#6f96b4')
        frame_accion.pack(side=tk.RIGHT, padx=20, pady=20)

        # Botones
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
            command=self.ejecutar_busqueda,
            state=tk.DISABLED  # Deshabilitado hasta cargar el mapa
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
            self.ciudad = CiudadInteligente(archivo)  # Crear instancia de CiudadInteligente
            self.dibujar_mapa()
            self.menu_algoritmo.config(state=tk.NORMAL)
            self.boton_buscar.config(state=tk.NORMAL)
            self.mensaje_estado.config(text="Mapa cargado correctamente.")

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
                color = 'white'
                if valor == 0:
                    color = 'white'  
                elif valor == 1:
                    color = 'grey'
                elif valor == 2:
                    color = 'blue'  # Vehículo
                elif valor == 3:
                    color = 'orange'
                elif valor == 4:
                    color = 'red'      
                elif valor == 5:
                    color = 'purple'  # Pasajero
                elif valor == 6:
                    color = 'green'  # Destino
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                fila_rectangulos.append(rect)
            self.rectangulos.append(fila_rectangulos)

        # Cargar y colocar la imagen del pasajero (persona.png)
        try:
            imagen_persona_original = Image.open("images/persona.png")
            imagen_persona_redimensionada = imagen_persona_original.resize((self.tam_celda, self.tam_celda), Image.LANCZOS)
            self.imagen_persona = ImageTk.PhotoImage(imagen_persona_redimensionada)
            pasajero = self.ciudad.posicion_pasajero
            x_p = pasajero[1] * self.tam_celda + self.tam_celda / 2
            y_p = pasajero[0] * self.tam_celda + self.tam_celda / 2
            self.imagen_persona_id = self.canvas.create_image(x_p, y_p, image=self.imagen_persona)
        except Exception as e:
            print(f"Error al cargar la imagen 'persona.png': {e}")

        # Cargar y colocar la imagen de ubicación (ubicacion.png)
        try:
            imagen_ubicacion_original = Image.open("images/ubicacion.png")
            imagen_ubicacion_redimensionada = imagen_ubicacion_original.resize((self.tam_celda, self.tam_celda), Image.LANCZOS)
            self.imagen_ubicacion = ImageTk.PhotoImage(imagen_ubicacion_redimensionada)
            destino = self.ciudad.destino
            x_d = destino[1] * self.tam_celda + self.tam_celda / 2
            y_d = destino[0] * self.tam_celda + self.tam_celda / 2
            self.imagen_ubicacion_id = self.canvas.create_image(x_d, y_d, image=self.imagen_ubicacion)
        except Exception as e:
            print(f"Error al cargar la imagen 'ubicacion.png': {e}")

        # Cargar y colocar la imagen del vehículo (auto-inteligente.png)
        try:
            imagen_original = Image.open("images/auto-inteligente.png")
            imagen_redimensionada = imagen_original.resize((self.tam_celda, self.tam_celda), Image.LANCZOS)
            self.imagen_auto = ImageTk.PhotoImage(imagen_redimensionada)
            inicio = self.ciudad.posicion_vehiculo
            x = inicio[1] * self.tam_celda + self.tam_celda / 2
            y = inicio[0] * self.tam_celda + self.tam_celda / 2
            # Si ya existe una imagen, eliminarla
            if self.imagen_auto_id:
                self.canvas.delete(self.imagen_auto_id)
            self.imagen_auto_id = self.canvas.create_image(x, y, image=self.imagen_auto)
        except Exception as e:
            print(f"Error al cargar la imagen 'auto-inteligente.png': {e}")

    def ejecutar_busqueda(self):
        if not self.ciudad:
            messagebox.showerror("Error", "No se ha cargado ningún mapa.")
            return

        tipo_busqueda = self.tipo_busqueda.get()
        algoritmo = self.algoritmo.get()

        # Deshabilitar botones durante la búsqueda
        self.boton_buscar.config(state=tk.DISABLED)
        self.boton_cargar.config(state=tk.DISABLED)
        self.menu_busqueda.config(state=tk.DISABLED)
        self.menu_algoritmo.config(state=tk.DISABLED)

        # Resetear el contador de nodos
        self.ciudad.contador_nodos = 0

        if tipo_busqueda == "No informada" and algoritmo == "Amplitud":
            # Realizar la búsqueda por amplitud
            try:
                camino, nodos_expandidos, exploracion = self.ciudad.busqueda_amplitud_total()
            except AttributeError as e:
                messagebox.showerror("Error", f"Error en la búsqueda: {e}")
                # Habilitar botones nuevamente
                self.habilitar_botones()
                return

        elif tipo_busqueda == "No informada" and algoritmo == "Profundidad evitando ciclos":
            # Realizar la búsqueda por profundidad
            try:
                camino, nodos_expandidos, exploracion = self.ciudad.busqueda_profundidad_total()
            except AttributeError as e:
                messagebox.showerror("Error", f"Error en la búsqueda: {e}")
                # Habilitar botones nuevamente
                self.habilitar_botones()
                return

        elif tipo_busqueda == "No informada" and algoritmo == "Costo uniforme":
            # Realizar la búsqueda de costo uniforme
            try:
                camino, nodos_expandidos, costo_total, exploracion = self.ciudad.busqueda_costo_uniforme_total()
            except AttributeError as e:
                messagebox.showerror("Error", f"Error en la búsqueda: {e}")
                # Habilitar botones nuevamente
                self.habilitar_botones()
                return
        elif tipo_busqueda == "Informada" and algoritmo == "Avara":
            # Realizar la búsqueda avara
            try:
                camino, nodos_expandidos, exploracion = self.ciudad.busqueda_avara_total()
            except AttributeError as e:
                messagebox.showerror("Error", f"Error en la búsqueda: {e}")
                # Habilitar botones nuevamente
                self.habilitar_botones()
                return

        else:
            messagebox.showerror("Error", "Algoritmo no implementado o incorrecto.")
            self.habilitar_botones()
            return

        if not camino:
            messagebox.showerror("Error", "No se encontró un camino válido.")
            self.habilitar_botones()
            return

        # Iniciar la animación de la búsqueda
        self.exploracion = exploracion
        self.camino = camino
        self.nodos_expandidos = nodos_expandidos
        self.paso_actual = 0
        self.dibujar_mapa()
        self.animar_busqueda()

    def habilitar_botones(self):
        # Habilitar botones nuevamente
        self.boton_buscar.config(state=tk.NORMAL)
        self.boton_cargar.config(state=tk.NORMAL)
        self.menu_busqueda.config(state=tk.NORMAL)
        self.menu_algoritmo.config(state=tk.NORMAL)


    def animar_busqueda(self):
        if self.paso_actual < len(self.exploracion):
            nodo = self.exploracion[self.paso_actual]
            fila, columna = nodo
            rect = self.rectangulos[fila][columna]
            # Color de exploración (por ejemplo, azul claro)
            self.canvas.itemconfig(rect, fill='lightblue')
            self.paso_actual += 1
            # Programar el siguiente paso
            self.ventana.after(50, self.animar_busqueda)  # Ajusta el tiempo según prefieras
        else:
            # Dibujar el camino final
            self.dibujar_camino(self.camino)
            mensaje = f"Algoritmo: Amplitud\nNodos expandidos: {self.nodos_expandidos}"
            self.mensaje_estado.config(text=mensaje)
            # Iniciar la animación de movimiento del auto
            self.mover_imagen(self.camino)
            # Habilitar botones nuevamente
            self.boton_buscar.config(state=tk.NORMAL)
            self.boton_cargar.config(state=tk.NORMAL)
            self.menu_busqueda.config(state=tk.NORMAL)
            self.menu_algoritmo.config(state=tk.NORMAL)

    def dibujar_camino(self, camino):
        if camino:
            for (fila, columna) in camino:
                rect = self.rectangulos[fila][columna]
                # Evitar colorear el inicio, pasajero y destino nuevamente
                valor = self.ciudad.mapa[fila][columna]
                if valor not in [2, 5, 6]:
                    self.canvas.itemconfig(rect, fill="yellow")
            # Resaltar el inicio, pasajero y destino con colores específicos
            inicio = self.ciudad.posicion_vehiculo
            pasajero = self.ciudad.posicion_pasajero
            destino = self.ciudad.destino
            self.canvas.itemconfig(self.rectangulos[inicio[0]][inicio[1]], fill='blue')
            self.canvas.itemconfig(self.rectangulos[pasajero[0]][pasajero[1]], fill='purple')
            self.canvas.itemconfig(self.rectangulos[destino[0]][destino[1]], fill='green')

    def mover_imagen(self, camino, index=0):
        if index < len(camino):
            fila, columna = camino[index]
            x = columna * self.tam_celda + self.tam_celda / 2
            y = fila * self.tam_celda + self.tam_celda / 2
            self.canvas.coords(self.imagen_auto_id, x, y)

            # Verificar si ha llegado al pasajero para eliminar la imagen del pasajero
            if (fila, columna) == self.ciudad.posicion_pasajero and self.imagen_persona_id:
                self.canvas.delete(self.imagen_persona_id)
                self.imagen_persona_id = None  # Evitar intentos de eliminación posteriores

            # Verificar si ha llegado al destino para superponer la imagen del pasajero y ocultar ubicacion.png
            if (fila, columna) == self.ciudad.destino:
                # Cargar y superponer la imagen del pasajero sobre el auto
                try:
                    imagen_persona_original = Image.open("images/persona.png")
                    imagen_persona_redimensionada = imagen_persona_original.resize((self.tam_celda, self.tam_celda), Image.LANCZOS)
                    self.imagen_persona_destino = ImageTk.PhotoImage(imagen_persona_redimensionada)
                    # Crear la imagen del pasajero superpuesta al auto
                    self.imagen_persona_destino_id = self.canvas.create_image(x, y, image=self.imagen_persona_destino)
                except Exception as e:
                    print(f"Error al cargar la imagen 'persona.png' en el destino: {e}")

                # Ocultar la imagen de ubicación (ubicacion.png)
                if self.imagen_ubicacion_id:
                    self.canvas.itemconfigure(self.imagen_ubicacion_id, state='hidden')

            # Programar el siguiente movimiento
            self.ventana.after(100, lambda: self.mover_imagen(camino, index + 1))
        else:
            # Llegó al destino
            print("El auto ha llegado al destino.")
            # Opcional: Puedes realizar acciones adicionales aquí si lo deseas

if __name__ == "__main__":
    InterfazCiudadGUI()
