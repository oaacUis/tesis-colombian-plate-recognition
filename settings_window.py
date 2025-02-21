#settings_window.py

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)
        
        self.days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        self.day_inputs = {}
        self.model_plate = "Normal"  # Valor por defecto para el modelo
        self.settings = {}  # Inicializa la configuración de Pico y Placa a vacío
        
        layout = QVBoxLayout()
        
        # Título para la configuración de Pico y Placa
        title_label = QLabel("Configuración de Pico y Placa")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title_label)
        
        # Sección de configuración de Pico y Placa
        for day in self.days:
            day_layout = QtWidgets.QHBoxLayout()
            label = QLabel(day)
            input1 = QLineEdit()
            input2 = QLineEdit()
            input1.setFixedWidth(50)
            input2.setFixedWidth(50)
            day_layout.addWidget(label)
            day_layout.addWidget(input1)
            day_layout.addWidget(input2)
            layout.addLayout(day_layout)
            self.day_inputs[day] = (input1, input2)
        
        # Botón Save para Pico y Placa
        self.save_button = QPushButton("Save Pico y Placa")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button, alignment=QtCore.Qt.AlignCenter)
        
        # Separador visual
        separator = QLabel("––––––––––––––––––––––––––––")
        separator.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(separator)
        
        # Sección para elegir modelo
        model_label = QLabel("Elegir modelo:")
        model_label.setAlignment(QtCore.Qt.AlignCenter)
        model_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(model_label)
        
        # Combo box para los modelos
        self.model_combo = QtWidgets.QComboBox()
        self.model_combo.addItems(["Normal", "Mejor", "Excelente"])
        layout.addWidget(self.model_combo)
        
        # # Botón Save para modelo (guardar de forma independiente)
        # self.save_model_button = QPushButton("Save Modelo")
        # self.save_model_button.clicked.connect(self.save_model_selection)
        # layout.addWidget(self.save_model_button, alignment=QtCore.Qt.AlignCenter)
        
        # Conexión a actualización inmediata (opcional)
        self.model_combo.currentTextChanged.connect(self.update_model_selection)
        
        self.setLayout(layout)
        
        # (Opcional) Otro separador visual
        separator = QLabel("––––––––––––––––––––––––––––")
        separator.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(separator)
    
    def update_model_selection(self, text):
        self.model_plate = text
        print("Modelo seleccionado:", self.model_plate)
    
    def save_model_selection(self):
        # Guarda la opción actual del modelo y muestra un mensaje (sin cerrar la ventana)
        self.model_plate = self.model_combo.currentText()
        print("Modelo guardado:", self.model_plate)
        QMessageBox.information(self, "Save Modelo", f"Modelo guardado: {self.model_plate}")
    
    def save_settings(self):
        # Guarda la configuración de Pico y Placa si el usuario la completa y cierra el diálogo
        settings = {}
        for day, inputs in self.day_inputs.items():
            input1 = inputs[0].text()
            input2 = inputs[1].text()
            if not input1.isdigit() or not input2.isdigit() or input1 == input2:
                QMessageBox.warning(self, "Error", f"Ingrese dos números diferentes para {day}.")
                return
            settings[day] = (int(input1), int(input2))
        self.settings = settings
        self.accept()  # Cierra el diálogo
        self.close()
    
    def reject(self):
        # Si se cierra la ventana sin pulsar Save, se devuelve la selección actual
        self.accept()
    
    def get_settings(self):
        return self.settings, self.model_plate