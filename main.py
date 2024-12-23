import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

def on_button_click():
    label.setText("Bouton cliqué!")
    
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("test")
window.setGeometry(100, 100, 400, 300)

central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout()

label = QLabel("Bienvenue dans PyQt5")
layout.addWidget(label)

button = QPushButton("Cliquez ici")
button.clicked.connect(on_button_click)
layout.addWidget(button)

central_widget.setLayout(layout)

window.show()

sys.exit(app.exec_())