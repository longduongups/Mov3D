# Nouvelle version de ui_main_posture pour projet "Correction de posture"
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class Ui_MainWindow_Posture(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self.centralwidget)

        # Titre
        self.title_label = QLabel("Correction de Posture", self.centralwidget)
        font_title = QFont()
        font_title.setPointSize(16)
        font_title.setBold(True)
        self.title_label.setFont(font_title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Boutons de contrôle
        self.button_layout = QHBoxLayout()

        self.btn_start_acquisition = QPushButton("Démarrer", self.centralwidget)
        self.btn_start_acquisition.setObjectName("btn_start_acquisition")
        self.button_layout.addWidget(self.btn_start_acquisition)

        self.btn_calibrate_sensors = QPushButton("Calibrer", self.centralwidget)
        self.btn_calibrate_sensors.setObjectName("btn_calibrate_sensors")
        self.button_layout.addWidget(self.btn_calibrate_sensors)

        self.btn_stop_acquisition = QPushButton("Arrêter", self.centralwidget)
        self.btn_stop_acquisition.setObjectName("btn_stop_acquisition")
        self.button_layout.addWidget(self.btn_stop_acquisition)

        self.main_layout.addLayout(self.button_layout)

        # Label d'avertissement
        self.label_angle_warning = QLabel("", self.centralwidget)
        self.label_angle_warning.setObjectName("label_angle_warning")
        font_warning = QFont()
        font_warning.setPointSize(11)
        font_warning.setBold(True)
        self.label_angle_warning.setFont(font_warning)
        self.label_angle_warning.setStyleSheet("color: red;")
        self.label_angle_warning.setAlignment(Qt.AlignCenter)
        self.label_angle_warning.setVisible(False)
        self.main_layout.addWidget(self.label_angle_warning)

        # Appliquer le layout principal
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Posture Tracker")
