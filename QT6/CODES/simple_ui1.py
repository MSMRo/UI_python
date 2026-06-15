import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class MiApp(QWidget):
    def __init__(self):
        super().__init__()  # Inicializa la configuración base de PyQt
        
        # 1. Configurar la ventana
        self.setWindowTitle("App Profesional en PyQt6")
        self.resize(300, 200)
        
        # 2. Crear un Layout (organizador) y los elementos
        layout = QVBoxLayout()
        self.etiqueta = QLabel("¡Hola, mundo desde una clase!")
        
        # 3. Ensamblar todo
        layout.addWidget(self.etiqueta)
        self.setLayout(layout)

# 4. Bloque de ejecución principal
if __name__ == "__main__":
    app = QApplication(sys.argv) # Inicia el motor de PyQt
    ventana = MiApp()            # Creamos la instancia de nuestra clase
    ventana.show()               # Mostramos la ventana
    sys.exit(app.exec())         # Ejecutamos el ciclo de la aplicación