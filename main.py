# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
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
import TestNvTrame_3
from posture_monitor import start_monitoring, stop_monitoring, calibrate, check_posture
# IMPORT / GUI AND MODULES AND WIDGETS
import threading
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from PyQt6.QtCore import pyqtSignal
from pyqtgraph import PlotWidget
from test import PieChartWidget
from modules.ui_main import Ui_MainWindow

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

#multithreading pour lire les datas

        


class MainWindow(QMainWindow):
    def __init__(self):
        self.thread = None
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.count=0

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Mov3D"
        description = "A Vectory3 project"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        widgets.btn_start_posture.clicked.connect(lambda: threading.Thread(target=start_monitoring).start())
        widgets.btn_stop_posture.clicked.connect(stop_monitoring)
        widgets.btn_calibrate_posture.clicked.connect(calibrate)
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.pushButton_2.clicked.connect(self.buttonClick)
        widgets.graphicsView_2.setVisible(False)
        widgets.graphicsView_2 = PieChartWidget()
        widgets.graphicsView_2.resize(400, 350)
        widgets.graphicsView_2.initUI()
        widgets.graphicsView_2.add_data(30,60)
        widgets.btn_pie.clicked.connect(self.buttonClick)
        widgets.pushButton_3.clicked.connect(self.buttonClick)
        widgets.label_7.setVisible(False)
        #widgets.btn_srate.clicked.connect(self.buttonClick)
        
        #widgets.graphicsView_rate = cadence.LineChartWidget()
    
        # widgets.graphicsView_rate.setVisible(False)
        # widgets.graphicsView_rate.resize(400, 350)
        self.graphicsView = widgets.graphicsView 
        #widgets.btn_enr.clicked.connect(self.buttonClick)
        #widgets.update_malloc.clicked.connect(self.buttonClick)


        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = True
        # themeFile = "themes\py_dracula_light.qss"
        themeFile = r"themes\mov3d_dark.qss"
        

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
    def update_posture_ui():
        if not check_posture():
            widgets.label_posture.setText("❌ Mauvaise posture détectée")
        else:
            widgets.label_posture.setText("✅ Posture correcte")
        QTimer.singleShot(500, update_posture_ui)
    update_posture_ui()    
    #Calcul de la vitesse et de la position à un point
    def integrate_acceleration(self,acceleration_values, time_interval):
        #Initialisation des valeurs de vitesse et de position
        velocity = [0, 0, 0]  # m/s
        position = [0, 0, 0]  # m

        #Intégration de l'accélération pour chaque axe (x, y, z)
        # Intégration numérique de l'accélération en vitesse (m/s)
        velocity[0] += acceleration_values[0] * time_interval
        velocity[1] += acceleration_values[1] * time_interval
        velocity[2] += acceleration_values[2] * time_interval

        #Intégration numérique de la vitesse en position (m)
        position[0] += velocity[0] * time_interval
        position[1] += velocity[1] * time_interval
        position[2] += velocity[2] * time_interval

        return velocity, position

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.label_7.setVisible(False)
            self.listeTables = np.array([])
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            
            self.db_name = "Data_IMU.db"
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
          

            widgets.comboBox_2.clear()
            for cpt in range(len(tables)) :
                widgets.comboBox_2.addItem(tables[cpt][0])

            #Variables qui définissent les métriques affichées
            self.output3d = 0
            self.outputsRate = 0


        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.enregistrements) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
    
        if btnName=="pushButton_3":            
            widgets.label_6.setStyleSheet("font: 24pt;")
            
            subprocess.run(["python", "./TestNvTrame_3.py"])
            widgets.label_7.setStyleSheet("font: 24pt;")
            widgets.label_7.setText("Go check your data !")
            widgets.label_7.setVisible(True)

            
        
        if btnName == "btn_pie":
            self.output3d = 1
            self.outputsRate = 1

        if btnName == "update_malloc":
            self.output3d = (self.output3d+1)%2
        
        if btnName == "btn_srate":
            self.outputsRate = (self.outputsRate+1)%2
            print(self.outputsRate)
            
        #Bouton récupérer données
        if btnName == "pushButton_2":

            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM "+widgets.comboBox_2.currentText() + " ORDER by time ASC;")
            rows = cursor.fetchall()

            timestamp_seconds = time.time()

            # Convertir le timestamp en dixièmes de seconde
            timestamp_tenth_seconds = int(timestamp_seconds * 10)

            nb_pasgauche = 0
            pasbase_gauche = 0
            initgauche = 0
            pasbase_droite = 0
            initdroite = 0
            nb_pasdroit = 0
            delai_gauche = 0
            delai_droite = 0
            last_timer_gauche = 0
            last_timer_droite = 0

            #variables 3D
            angleCuisseG = angleCuisseD = angleTibG = angleTibD = 0
            line_thigh1,line_calf1,hip_joint1,knee_joint1,ankle_joint1,line_thigh2,line_calf2,hip_joint2,knee_joint2,ankle_joint2,line_leg_connector,fig = message.init_jambes()

            #Variables cadance
            point_avant = [0,0]
            ax = cadence.init_graph()
            totalpasavant = 0

            #Variables symetrie
            axSymetrie = symetrie.init_graph()


            timestamp_debut = int(time.time() * 1000)

            #Données durée du cycle de marche
            cycleY = np.array([])

            #Données accel, vitesse et position
            oldtime_left = 0
            oldtime_right = 0
            posleft_init = 0
            posright_init = 0
            acc_x_l = 0
            acc_y_l = 0
            acc_z_l = 0
            acc_x_r = 0
            acc_y_r = 0
            acc_z_r = 0
            disttotale_left = 0
            disttotale_right = 0

            for i in range(len(rows)):

                test = False
                while(test == False):
                    test = int(time.time()*1000)-timestamp_debut >= int(rows[i][1])-int(rows[0][1])
                
                # print("---------")
                # print(rows[i])
                #Partie détection pas
                nouveaupas = delaipas = 0
            
                if(rows[i][2] == "Cuisse_Droite"):
                    if(initdroite == 0):
                        initdroite = 1
                        pasbase_droite = rows[i][12]
                    
                    angleCuisseD = rows[i][10]
                    
                    ecart = rows[i][1] - last_timer_droite
                    last_timer_droite = rows[i][1]
                    delai_droite = delai_droite + ecart
                    if(rows[i][12] > nb_pasdroit+pasbase_droite):
                        nouveaupas = 1
                        delaipas = delai_droite
                        # print("Pas à droite")
                        # print(delai_droite)
                        delai_droite = 0
                        nb_pasdroit+=1
                elif(rows[i][2] == "Cuisse_Gauche"):
                    if(initgauche == 0):
                        initgauche = 1
                        pasbase_gauche = rows[i][12]

                    angleCuisseG = rows[i][10]
                   
                    ecart = rows[i][1] - last_timer_gauche
                    last_timer_gauche = rows[i][1]
                    delai_gauche = delai_gauche + ecart
                    if(rows[i][12] > nb_pasgauche+pasbase_gauche):
                        nouveaupas = 1
                        delaipas = delai_gauche
                        # print("Pas à gauche")
                        # print(delai_gauche)
                        delai_gauche = 0
                        nb_pasgauche+=1
                elif(rows[i][2] == "Tibia_Droit"):
                    angleTibD = rows[i][10]
                elif(rows[i][2] == "Tibia_Gauche"):
                    angleTibG = rows[1][10]


                #Calculs accélération
                if(rows[i][2] == "Cuisse_Droite"):
                    if(posright_init == 1): 
                        velocity, position = self.integrate_acceleration([acc_x_r,acc_y_r,acc_z_r],(rows[i][1]-oldtime_right)/1000.0)#
                        disttotale_right = disttotale_right + math.sqrt(position[0]**2+position[1]**2)
                        acc_x_r = rows[i][3]#*9.80665 #-> acc_x est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_y_r = rows[i][4]#*9.80665 #-> acc_y est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_z_r = rows[i][5]#*9.80665 #-> acc_z est en g, on multiplie par 9.80665 pour passer en m/s²
                        oldtime_right = rows[i][1]

                    else:
                        posright_init = 1
                        oldtime_right = rows[i][1]
                        acc_x_r = rows[i][3]#*9.80665 #-> acc_x est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_y_r = rows[i][4]#*9.80665 #-> acc_y est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_z_r = rows[i][5]#*9.80665 #-> acc_z est en g, on multiplie par 9.80665 pour passer en m/s²

                if(rows[i][2] == "Cuisse_Gauche"):
                    if(posleft_init == 1):
                        velocity, position = self.integrate_acceleration([acc_x_l,acc_y_l,acc_z_l],(rows[i][1]-oldtime_left)/1000.0)#
                        oldtime_left = rows[i][1]
                        disttotale_left = disttotale_left + math.sqrt(position[0]**2+position[1]**2)
                        acc_x_l = rows[i][3]#*9.80665 #-> acc_x est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_y_l = rows[i][4]#*9.80665 #-> acc_y est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_z_l = rows[i][5]#*9.80665 #-> acc_z est en g, on multiplie par 9.80665 pour passer en m/s²
                        
                    else:
                        posleft_init = 1
                        oldtime_left = rows[i][1]
                        acc_x_l = rows[i][3]#*9.80665 #-> acc_x est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_y_l = rows[i][4]#*9.80665 #-> acc_y est en g, on multiplie par 9.80665 pour passer en m/s²
                        acc_z_l = rows[i][5]#*9.80665 #-> acc_z est en g, on multiplie par 9.80665 pour passer en m/s²
                        
                


                #Partie cycle de marche
                if(nouveaupas == 1):

                    if(i>0):
                        delta_temps = delaipas
                        cycleY = np.append(cycleY,delta_temps)
                    
                    if(len(cycleY) > 0):

                        if(len(cycleY)>3):
                            cycleY = cycleY[1:]             
                        self.graphicsView.clear()
                        if(len(cycleY)>0):
                            self.graphicsView.plot([1,1],[0,cycleY[0]],pen=1+i)
                        if(len(cycleY)>1):
                            self.graphicsView.plot([2,2],[0,cycleY[1]],pen=2+i)
                        if(len(cycleY)>2):
                            self.graphicsView.plot([3,3],[0,cycleY[2]],pen=3+i)
                ##############


                # if(nb_pasgauche>0 or nb_pasdroit>0):
                    # print("Total pas : "+str(nb_pasgauche)+"/"+str(nb_pasdroit))
                    # print("Répartition pas : ",nb_pasgauche*100/(nb_pasgauche+nb_pasdroit),"%","/",nb_pasdroit*100/(nb_pasgauche+nb_pasdroit),"%")

                


                #Partie cadence
                if(i%2==1 and self.outputsRate == 1):
                    totalpas = nb_pasdroit + nb_pasgauche
                    temps = rows[i][1]/1000 - rows[0][1]/1000 + 0.0001
                    point = [temps,totalpas/2*60/temps]
                    if(totalpasavant != totalpas):
                        #Test symétrie
                        if(nb_pasgauche == 0 and disttotale_left > 0 and (disttotale_left + disttotale_right) > 0):
                            symetrie.printplt(axSymetrie,0,(disttotale_left+disttotale_right)/(nb_pasgauche+nb_pasdroit))
                        elif(disttotale_left > 0 and disttotale_right > 0 and (disttotale_left + disttotale_right) > 0):
                            symetrie.printplt(axSymetrie,disttotale_left/nb_pasgauche,disttotale_right/+nb_pasdroit)
                        symetrie.plt.draw()
                        symetrie.plt.pause(0.005)

                        cadence.printplt(point_avant,point,ax)
                        cadence.plt.draw()
                        cadence.plt.pause(0.005)
                        point_avant = point
                    totalpasavant = totalpas
                

                #Partie 3D
                if(i%2==1 and self.output3d == 1):
                    self.l_jambe = [angleCuisseG,angleTibG,angleCuisseD-75,angleTibD+80]
                    message.update_leg(self.l_jambe[0]-90,self.l_jambe[1]+90,self.l_jambe[2],self.l_jambe[3],line_thigh1,line_calf1,hip_joint1,knee_joint1,ankle_joint1,line_thigh2,line_calf2,hip_joint2,knee_joint2,ankle_joint2,line_leg_connector,fig)
                    message.plt.draw()
                    message.plt.pause(0.1)
                
                #Nombre de pas
                widgets.label_5.setText(str(math.floor(nb_pasgauche/2)) + " / " + str(math.floor(nb_pasdroit/2)))

                QApplication.processEvents()

                # print("---------")
            print("TEST")
            widgets.label_5.setText(str(math.floor(nb_pasgauche/2)) + " / " + "4")
            print(str(nb_pasdroit)+ " " +str(nb_pasgauche))
            print("Dist totale gauche = " + str(disttotale_left))
            print("Dist totale droite = " + str(disttotale_right))
            print("finito")
    
        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        # if event.buttons() == Qt.LeftButton:
        #     print('Mouse click: LEFT CLICK')
        # if event.buttons() == Qt.RightButton:
        #     print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    if QApplication.instance():
    # If there is, quit the existing instance
        QApplication.instance().quit()

    app = QApplication()
    # app.setWindowIcon(QIcon("icon.ico"))
    app.setWindowIcon(QIcon("vectory3.ico"))
    window = MainWindow()
    sys.exit(app.exec())
