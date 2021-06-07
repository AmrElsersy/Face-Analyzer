import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QIcon, QPen



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.styles = {}

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)


    def update_graph(self, model_data: list):
        pass

    
# class MainWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         self.FER_2013_EMO_DICT = {
#             0: "Angry",
#             1: "Disgust",
#             2: "Fear",
#             3: "Happy",
#             4: "Sad",
#             5: "Surprise",
#             6: "Neutral",
#         }

#         # window requirements
#         self.setGeometry(200,200,600,400)
#         self.setWindowTitle("Emotions")
#         self.setWindowIcon(QIcon("python.png"))
    
#         # change the color of the window
#         self.setStyleSheet('background-color:white')
 
 
#         #create QChart object
#         chart = QChart()
#         chart.addSeries(self.plot_widget())
#         chart.setAnimationOptions(QChart.SeriesAnimations)
#         chart.setTitle("Fruits Pie Chart")
#         chart.setTheme(QChart.ChartThemeQt)
        
#         chartview = QChartView(chart)

#         new_series  = QPieSeries()
#         new_series.append("aroma", 10)
#         new_series.append("aromaX", 20)
#         new_chart = QChart()
#         new_chart.addSeries(new_series)

#         vbox = QHBoxLayout()
#         vbox.addWidget(chartview)
#         vbox.addWidget(QChartView(new_chart))
 
#         self.setLayout(vbox)

#     def create_emotions_chart(self):
#         pass
    
#     def plot_widget(self, new_data=None):
#         #create pieseries
#         series  = QPieSeries()
 
        
#         for item in self.FER_2013_EMO_DICT.keys():
#             series.append(self.FER_2013_EMO_DICT[item], 50)

#         #slice
#         my_slice = series.slices()[3]
#         my_slice.setExploded(True)
#         my_slice.setLabelVisible(True)
#         my_slice.setPen(QPen(Qt.green, 4))
#         my_slice.setBrush(Qt.green)

#         return series
 

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    # main = MainWidget()
    main.show()
    sys.exit(app.exec_())
    
    
    

if __name__ == "__main__":
    main()
        

