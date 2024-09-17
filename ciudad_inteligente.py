import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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

if __name__ == "__main__":
    InterfazCiudad()
