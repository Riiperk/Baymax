import tkinter as tk
import math
import random
import threading

# Variable global que actuará como "puente" entre el cerebro y el rostro
_estado_actual = "neutral"

def actualizar_rostro(nuevo_estado):
    """
    Función pública que usará main.py para cambiar la expresión de Bayx.
    Estados válidos: 'neutral', 'escuchando', 'hablando', 'musica'
    """
    global _estado_actual
    _estado_actual = nuevo_estado

class RostroBaymax:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("SISTEMA MÉDICO BAYX - HUD VISUAL")
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        
        # Elimina los bordes de la ventana si lo quieres en pantalla completa (opcional)
        # self.root.attributes('-fullscreen', True)

        # Lienzo (Canvas) donde dibujaremos el rostro
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")

        # Variables de control de animación
        self.frame = 0.0
        
        # Coordenadas y proporciones exactas de la película
        self.centro_x = 400
        self.centro_y = 300
        self.distancia_ojos = 140 # Distancia del centro a cada ojo
        self.radio_base = 45      # Tamaño original de los ojos
        self.grosor_base = 6      # Grosor de la línea conectora

        # 1. Dibujamos la línea conectora
        self.linea = self.canvas.create_line(
            self.centro_x - self.distancia_ojos, self.centro_y, 
            self.centro_x + self.distancia_ojos, self.centro_y, 
            fill="white", width=self.grosor_base, capstyle=tk.ROUND
        )
        
        # 2. Dibujamos el ojo izquierdo
        self.ojo_izq = self.canvas.create_oval(
            self.centro_x - self.distancia_ojos - self.radio_base, self.centro_y - self.radio_base, 
            self.centro_x - self.distancia_ojos + self.radio_base, self.centro_y + self.radio_base, 
            fill="white", outline="white"
        )
        
        # 3. Dibujamos el ojo derecho
        self.ojo_der = self.canvas.create_oval(
            self.centro_x + self.distancia_ojos - self.radio_base, self.centro_y - self.radio_base, 
            self.centro_x + self.distancia_ojos + self.radio_base, self.centro_y + self.radio_base, 
            fill="white", outline="white"
        )

        # Iniciamos el motor de renderizado (60 FPS aproximados)
        self.animar()

    def animar(self):
        """Motor matemático para animar el rostro frame a frame."""
        global _estado_actual
        self.frame += 0.1
        
        # Variables por defecto para cada frame
        color_actual = "white"
        grosor = self.grosor_base
        radio_x = self.radio_base
        radio_y = self.radio_base # Separamos X y Y para poder hacer el parpadeo

        # --- LÓGICA DE ESTADOS ---
        if _estado_actual == "escuchando":
            # Pulso suave y lento como respiración
            pulso = math.sin(self.frame * 1.5) * 6
            radio_x += pulso
            radio_y += pulso

        elif _estado_actual == "hablando":
            # La línea vibra simulando frecuencias de voz
            grosor = self.grosor_base + abs(math.sin(self.frame * 4)) * 6
            color_actual = "#f0f0f0" # Un blanco ligeramente más opaco

        elif _estado_actual == "musica":
            # Tono azul cian de salud y pulsaciones rítmicas
            color_actual = "#00BFFF" 
            pulso = math.sin(self.frame * 2.5) * 8
            radio_x += pulso
            radio_y += pulso
            grosor = self.grosor_base + 2

        else: # Estado "neutral"
            # Parpadeo aleatorio orgánico
            if random.random() < 0.015: 
                radio_y = 2 # Aplasta el óvalo en Y para simular ojos cerrados

        # --- APLICAR TRANSFORMACIONES AL CANVAS ---
        
        # Actualizar Ojo Izquierdo
        self.canvas.coords(
            self.ojo_izq, 
            self.centro_x - self.distancia_ojos - radio_x, self.centro_y - radio_y, 
            self.centro_x - self.distancia_ojos + radio_x, self.centro_y + radio_y
        )
        
        # Actualizar Ojo Derecho
        self.canvas.coords(
            self.ojo_der, 
            self.centro_x + self.distancia_ojos - radio_x, self.centro_y - radio_y, 
            self.centro_x + self.distancia_ojos + radio_x, self.centro_y + radio_y
        )
        
        # Actualizar Línea y Colores
        self.canvas.itemconfig(self.linea, width=grosor, fill=color_actual)
        self.canvas.itemconfig(self.ojo_izq, fill=color_actual, outline=color_actual)
        self.canvas.itemconfig(self.ojo_der, fill=color_actual, outline=color_actual)

        # Repetir el bucle cada 30 milisegundos
        self.root.after(30, self.animar)

    def iniciar(self):
        """Inicia el bucle de la interfaz gráfica."""
        self.root.mainloop()

# =================================================================
# LANZADOR EN HILO SECUNDARIO (Para no bloquear el Cerebro)
# =================================================================
def iniciar_interfaz_en_hilo():
    """Ejecuta la ventana en un hilo separado de Windows."""
    def correr():
        app = RostroBaymax()
        app.iniciar()
    
    hilo_gui = threading.Thread(target=correr, daemon=True)
    hilo_gui.start()

# =================================================================
# ZONA DE PRUEBAS (Test Mode)
# =================================================================
if __name__ == "__main__":
    # Si ejecutas este archivo directamente, se abrirá un panel de pruebas
    def test_neutral(): actualizar_rostro("neutral")
    def test_escuchando(): actualizar_rostro("escuchando")
    def test_hablando(): actualizar_rostro("hablando")
    def test_musica(): actualizar_rostro("musica")

    # Arrancamos la interfaz principal
    iniciar_interfaz_en_hilo()

    # Creamos una ventanita extra para los botones de prueba
    panel = tk.Tk()
    panel.title("Panel de Control")
    panel.geometry("250x200")
    panel.configure(bg="#222")

    tk.Label(panel, text="Prueba de Animaciones:", fg="white", bg="#222").pack(pady=10)
    tk.Button(panel, text="1. Neutral", command=test_neutral, width=20).pack(pady=2)
    tk.Button(panel, text="2. Escuchando", command=test_escuchando, width=20).pack(pady=2)
    tk.Button(panel, text="3. Hablando", command=test_hablando, width=20).pack(pady=2)
    tk.Button(panel, text="4. Terapia Musical", command=test_musica, width=20).pack(pady=2)

    panel.mainloop()