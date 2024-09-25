import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from nodo import Nodo
from busqueda_no_informada import busqueda_profundidad_eviar_ciclos
from leer_mapa import leer_mapa

class InterfazCiudad:
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

    #Botones
        self.boton_cargar = tk.Button(
            frame_accion,
            text="Cargar Archivo",
            font=fuente_fresca,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            width=15
        )
        self.boton_cargar.pack(side=tk.LEFT, padx=5)

        self.boton_buscar = tk.Button(
            frame_accion,
            text="Buscar y Llevar",
            font=fuente_fresca,
            bg='#008CBA',
            fg='white',
            activebackground='#007bb5',
            width=15
        )
        self.boton_buscar.pack(side=tk.LEFT, padx=5)

        self.mensaje_estado = tk.Label(
            self.content_frame,
            text="",
            font=fuente_fresca,
            bg='#dad082'
        )
        self.mensaje_estado.pack(side=tk.BOTTOM, fill='x')

    def cargar_archivo(self):
        self.archivo_mapa = filedialog.askopenfilename(
            title="Seleccionar archivo de mapa",
            filetypes=(("Archivos de texto", "*.txt"),("Todos los archivos", "*.*"))
        )
        if not self.archivo_mapa:
            messagebox.showerror("Error", "Debe seleccionar un archivo de mapa")
        else:
            try:
                self.ciudad = leer_mapa(self.archivo_mapa)
                print(self.ciudad)
                self.mostrar_mapa()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    def mostrar_mapa(self):
        if self.ciudad: # Si hay un mapa cargado
            self.canvas.delete("all")
            for i, fila in enumerate(self.ciudad): # Recorre las filas
                for j, valor in enumerate(fila): # Recorre los valores de la fila
                    color = self.obtener_color(valor) # Obtiene el color según el valor
                    self.canvas.create_rectangle( # Dibuja un rectángulo
                        j ** self.tam_celda, 
                        i ** self.tam_celda,
                        (j + 1) ** self.tam_celda,
                        (i + 1) ** self.tam_celda,
                        fill=color # Color del rectángulo
                    )
                    print(f"Dibuja celda ({i}, {j}) con color {color}")

    def obtener_color(self, valor):
        if valor == 0:
            return "white" # Trafico liviano/ Casilla blanca
        elif valor == 1:
            return "grey" #Muro/ Casilla gris
        elif valor == 2:
            return "yellow" #Vehiculo/ Casilla amarilla
        elif valor == 3:
            return "green" #Trafico mediano / Casilla verde
        elif valor == 4:
            return "red" #Trafico pesado / Casilla roja
        elif valor == 5:
            return "blue" #Pasajero / Casilla azul
        elif valor == 6:
            return "orange" #Destino / Casilla naranja        
        else:
            return "white"

    def buscar_camino(self):
        if self.ciudad is None:
            messagebox.showerror("Error", "Debe cargar un archivo de mapa")
            return
        
        nodo_inicial = Nodo(self.ciudad)

        if self.algoritmo.get() == "Búsqueda no informada - evitando ciclos":
            nodo_meta = busqueda_profundidad_evitar_ciclos(nodo_inicial)
        if nodo_meta:
            messagebox.showinfo("Información", "¡Solución encontrada!")
            self.mostrar_mapa_final(nodo_meta.obteenr_camino())
        else:
            maessagebox.showinfo("Información", "¡No se encontró solución!")

if __name__ == "__main__":
    InterfazCiudad()
