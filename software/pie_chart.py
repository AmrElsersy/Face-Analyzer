import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QIcon, QPen



class GazeTrackingChart(QWidget):
    def __init__(self):
        super(GazeTrackingChart, self).__init__()
        self.status = {
                0: "right",
                1: "left",
                2: "blink",
                3: "focus"
        }

        # window requirements
        # self.setGeometry(200,200,600,400)
        # self.setWindowTitle("Gaze-Tracking")
        # self.setWindowIcon(QIcon("chart.png"))

        # change the color of the window
        self.setStyleSheet('background-color:white')


        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setTitle("Gaze-Tracking Pie Chart")
        self.chart.setTheme(QChart.ChartThemeBrownSand)
        

        chartview = QChartView(self.chart)

        vbox = QHBoxLayout()
        vbox.addWidget(chartview)

        self.setLayout(vbox)


    # def __plot_widget(self, new_data=None):
    #     #create pieseries
    #     series  = QPieSeries()


    #     for item in self.FER_2013_EMO_DICT.keys():
    #         series.append(self.FER_2013_EMO_DICT[item], 50)

    #     #slice
    #     my_slice = series.slices()[3]
    #     my_slice.setExploded(True)
    #     my_slice.setLabelVisible(True)
    #     my_slice.setPen(QPen(Qt.green, 4))
    #     my_slice.setBrush(Qt.green)

    #     return series

    def add_data(self, data):
        # self.layout.itemAt(0).setParent(None)

        # data = self.__preprocess_data(data)
        series  = QPieSeries()
        for i in range(len(self.status.keys())):
            print(i)
            series.append(self.status[i], data[i])
        
        self.chart.addSeries(series)
        return series

    def __preprocess_data(self, raw_data):
        data = [0] * 4

        for el in raw_data:
            data[0] += el[self.status[0]]
            data[1] += el[self.status[1]]
            data[2] += el[self.status[2]]
            data[3] += el[self.status[3]]
        
        return data

    def __expand_slice(self):
        pass




# def main():
#     app = QApplication(sys.argv)
#     main = GazeTrackingChart()
#     # for i in range(5):
#     #     main.add_data([2,5,6,3])
#     # main = MainWidget()
#     main.show()
#     sys.exit(app.exec_())
    
    
    

# if __name__ == "__main__":
#     main()
        

