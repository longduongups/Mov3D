import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QPieSeries

class PieChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.move(0,500)
        self.series = QPieSeries()
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.layout = QVBoxLayout()
        self.chart.addSeries(self.series)
        self.layout.addWidget(self.chart_view)
        self.setLayout(self.layout)
        
        
        
        
    def add_data(self,gauche,total):
        print("camanbere")
        self.series.clear()
        self.series.append("Droite",int(total/(total-gauche)*100))
        if(gauche>0):
            self.series.append("Gauche",int(total/gauche*100))
        else : 
            self.series.append("Gauche",0)
        
        self.chart.createDefaultAxes()
        self.chart.setTitle("Symétrie de la marche")
        # file_name2= file_name+".txt"
        # for root, dirs, files in os.walk("./balance"):
        #     for file in files:
        #         if file.lower() == file_name2.lower():
        #             with open("./balance/" +file,"r") as f:
        #                 print(f.name)
        #                 content = f.readlines()
        #                 self.series.append("Right",int(content[0]))
        #                 self.series.append("Left", int(content[1]))
        #                 self.chart.addSeries(self.series)
        #                 self.chart.createDefaultAxes()
        #                 self.chart.setTitle(file_name)
        #                 print(content[0],content[1])
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PieChartWidget()
    window.show()

    sys.exit(app.exec())