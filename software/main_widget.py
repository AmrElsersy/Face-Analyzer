# from pyqtgraph import PlotWidget, plot
# import pyqtgraph as pg
# import required library for GUI
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5 import QtGui
# from PyQt5.QtChart import QChart, QChartView, QPieSeries
from live_graph import Live_Graph
import sys

class Live_Statistics(QWidget):
    def __init__(self):
        # call the constructor of the parent (QWidget)
        super(Live_Statistics, self).__init__()

        # set title  and geometry for the window
        self.setWindowTitle("Live Statistics")
        self.setGeometry(500, 400, 800, 600)

        # give orange background to the window
        palette = self.palette()
        palette.setColor(QPalette.Window,QColor(0, 128, 128))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # set minimum width and height for the window
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)
        self.setMaximumHeight(600)
        self.setMaximumWidth(800)

        # set icon for the application at run time and center the application window with the primary screen
        self.setIcon()
        self.center()

        self.createTabs()

    def createTabs(self):
        self.layout = QVBoxLayout()
        self.live_graph = Live_Graph()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.live_graph, QIcon("graph.png"), "Live Graph")
        self.tabs.addTab(QWidget(), QIcon("hist.png"), "Live Histogram")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # set icon for the application
    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    # to center the application window at the beginning
    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())


# class MainWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.FER_2013_EMO_DICT = {
#             0: "Angry",
#             1: "Disgust",
#             2: "Fear",
#             3: "Happy",
#             4: "Sad",
#             5: "Surprise",
#             6: "Neutral",
#         }
#
#         # window requirements
#         self.setGeometry(200,200,600,400)
#         self.setWindowTitle("Emotions")
#         self.setWindowIcon(QIcon("python.png"))
#
#         # change the color of the window
#         self.setStyleSheet('background-color:white')
#
#
#         #create QChart object
#         chart = QChart()
#         chart.addSeries(self.__plot_widget())
#         chart.setAnimationOptions(QChart.SeriesAnimations)
#         chart.setTitle("Fruits Pie Chart")
#         chart.setTheme(QChart.ChartThemeQt)
#
#         chartview = QChartView(chart)
#
#         new_series  = QPieSeries()
#         new_series.append("aroma", 10)
#         new_series.append("aromaX", 20)
#         new_chart = QChart()
#         new_chart.addSeries(new_series)
#
#         vbox = QHBoxLayout()
#         vbox.addWidget(chartview)
#         vbox.addWidget(QChartView(new_chart))
#
#         self.setLayout(vbox)
#
#
#     def __plot_widget(self, new_data=None):
#         #create pieseries
#         series  = QPieSeries()
#
#
#         for item in self.FER_2013_EMO_DICT.keys():
#             series.append(self.FER_2013_EMO_DICT[item], 50)
#
#         #slice
#         my_slice = series.slices()[3]
#         my_slice.setExploded(True)
#         my_slice.setLabelVisible(True)
#         my_slice.setPen(QPen(Qt.green, 4))
#         my_slice.setBrush(Qt.green)
#
#         return series
 

        

def main():
    app = QApplication(sys.argv)
    main = Live_Statistics()
    # main = MainWidget()
    main.show()
    sys.exit(app.exec_())
    
    
    

if __name__ == "__main__":
    main()
        

