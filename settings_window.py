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
        
        layout = QVBoxLayout()
        
        # Agregar un título al inicio
        title_label = QLabel("Configuración de Pico y Placa")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title_label)
        
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
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button, alignment=QtCore.Qt.AlignCenter)
        
        self.setLayout(layout)
    
    def save_settings(self):
        settings = {}
        for day, inputs in self.day_inputs.items():
            input1 = inputs[0].text()
            input2 = inputs[1].text()
            if not input1.isdigit() or not input2.isdigit() or input1 == input2:
                QMessageBox.warning(self, "Error", f"Ingrese dos números diferentes para {day}.")
                return
            settings[day] = (int(input1), int(input2))
        
        self.accept()
        self.settings = settings
        self.close()
    
    def get_settings(self):
        return self.settings