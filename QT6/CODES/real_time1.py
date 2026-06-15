import sys
import numpy as np
import neurokit2 as nk
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        pantalla = VisorSeñales()

        self.setCentralWidget(pantalla)

class VisorSeñales(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración principal de la ventana
        self.setWindowTitle("Monitor de Señal y FFT en Tiempo Real")
        self.resize(800, 600)
        
        # 2. Configuración de los datos (NeuroKit2)
        self.fs = 1000  # Frecuencia de muestreo (Hz)
        # Simulamos 5 minutos de ECG para tener suficientes datos
        self.senal_completa = nk.ecg_simulate(duration=300, sampling_rate=self.fs)
        self.indice_actual = 0
        self.tamano_ventana = self.fs * 2  # Mostraremos 2 segundos de señal a la vez
        
        # 3. Creación de los elementos de la UI (Layouts y Botones)
        layout_principal = QVBoxLayout()
        layout_botones = QHBoxLayout()
        
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pausa")
        
        layout_botones.addWidget(self.btn_play)
        layout_botones.addWidget(self.btn_pause)
        
        # 4. Configuración de Matplotlib dentro de PyQt6
        self.figura = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figura)
        
        # Crear dos subgráficas: Arriba (Tiempo) y Abajo (Frecuencia/FFT)
        self.ax_tiempo = self.figura.add_subplot(211)
        self.ax_fft = self.figura.add_subplot(212)
        
        # Ensamblar la interfaz
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.canvas)
        self.setLayout(layout_principal)
        
        # 5. Configurar el temporizador (Timer) para la animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_grafica)
        
        # 6. Conectar los botones a sus funciones
        self.btn_play.clicked.connect(self.iniciar)
        self.btn_pause.clicked.connect(self.pausar)

    def iniciar(self):
        # El timer se ejecuta cada 50 milisegundos
        self.timer.start(50)

    def pausar(self):
        # Detiene el temporizador
        self.timer.stop()

    def actualizar_grafica(self):
        # Extraer el fragmento actual de la señal
        fin = self.indice_actual + self.tamano_ventana
        
        # Si llegamos al final de la señal simulada, volvemos a empezar
        if fin > len(self.senal_completa):
            self.indice_actual = 0
            fin = self.tamano_ventana
            
        ventana_actual = self.senal_completa[self.indice_actual:fin]
        
        # Limpiar los ejes para el nuevo cuadro
        self.ax_tiempo.clear()
        self.ax_fft.clear()
        
        # --- DIBUJAR SEÑAL EN EL TIEMPO ---
        tiempo_eje = np.linspace(0, 2, self.tamano_ventana)
        self.ax_tiempo.plot(tiempo_eje, ventana_actual, color='blue')
        self.ax_tiempo.set_title("Señal ECG Simulada (NeuroKit2)")
        self.ax_tiempo.set_ylabel("Amplitud")
        self.ax_tiempo.set_xlabel("Tiempo (s)")
        
        # --- DIBUJAR LA FFT ---
        # Calcular frecuencias y magnitud usando NumPy
        frecuencias = np.fft.rfftfreq(self.tamano_ventana, d=1/self.fs)
        magnitud = np.abs(np.fft.rfft(ventana_actual))
        
        self.ax_fft.plot(frecuencias, magnitud, color='red')
        self.ax_fft.set_title("Transformada Rápida de Fourier (FFT)")
        self.ax_fft.set_ylabel("Magnitud")
        self.ax_fft.set_xlabel("Frecuencia (Hz)")
        self.ax_fft.set_xlim(0, 40) # Limitamos a 40Hz porque el ECG concentra su energía ahí
        
        # Ajustar espacios y mandar a dibujar
        self.figura.tight_layout()
        self.canvas.draw()
        
        # Avanzar el índice simulando el paso del tiempo real (50ms)
        avance = int(self.fs * 0.05) 
        self.indice_actual += avance

# 7. Bloque de ejecución principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow() #VisorSeñales()
    ventana.show()
    sys.exit(app.exec())