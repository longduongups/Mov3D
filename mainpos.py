# MODIFICATION main.py pour intégration du module posture

import sys
import subprocess
import os
import platform
import time
import mysql.connector
import numpy as np
import sqlite3
import message
import cadence
import symetrie
import math
import threading

# IMPORT / GUI AND MODULES AND WIDGETS
from modules import *
from widgets import *
from PyQt6.QtCore import pyqtSignal, QTimer
from pyqtgraph import PlotWidget
from test import PieChartWidget
from modules.ui_main import Ui_MainWindow

# Import du module de posture
from posture_monitor import start_monitoring, stop_monitoring, calibrate, check_posture

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        self.thread = None
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.count=0

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "Mov3D"
        description = "A Vectory3 project"
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        UIFunctions.uiDefinitions(self)

        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.pushButton_2.clicked.connect(self.buttonClick)
        widgets.btn_pie.clicked.connect(self.buttonClick)
        widgets.pushButton_3.clicked.connect(self.buttonClick)
        widgets.label_7.setVisible(False)

        widgets.graphicsView_2.setVisible(False)
        widgets.graphicsView_2 = PieChartWidget()
        widgets.graphicsView_2.resize(400, 350)
        widgets.graphicsView_2.initUI()
        widgets.graphicsView_2.add_data(30,60)

        self.graphicsView = widgets.graphicsView

        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        self.show()

        useCustomTheme = True
        themeFile = r"themes\mov3d_dark.qss"

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        # --- Connexion des boutons de la page posture ---
        widgets.btn_posture.clicked.connect(lambda: self.open_page(widgets.page_posture))
        widgets.btn_start_posture.clicked.connect(lambda: threading.Thread(target=start_monitoring).start())
        widgets.btn_stop_posture.clicked.connect(stop_monitoring)
        widgets.btn_calibrate_posture.clicked.connect(calibrate)

        def update_posture_ui():
            if check_posture():
                widgets.label_posture.setText("✅ Posture correcte")
            else:
                widgets.label_posture.setText("❌ Mauvaise posture détectée")
            QTimer.singleShot(500, update_posture_ui)
        update_posture_ui()

    def open_page(self, page):
        widgets.stackedWidget.setCurrentWidget(page)
        UIFunctions.resetStyle(self, self.sender().objectName())
        self.sender().setStyleSheet(UIFunctions.selectMenu(self.sender().styleSheet()))

    def integrate_acceleration(self,acceleration_values, time_interval):
        velocity = [0, 0, 0]
        position = [0, 0, 0]
        velocity[0] += acceleration_values[0] * time_interval
        velocity[1] += acceleration_values[1] * time_interval
        velocity[2] += acceleration_values[2] * time_interval
        position[0] += velocity[0] * time_interval
        position[1] += velocity[1] * time_interval
        position[2] += velocity[2] * time_interval
        return velocity, position

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_new":
            widgets.label_7.setVisible(False)
            self.listeTables = np.array([])
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
