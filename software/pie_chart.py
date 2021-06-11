from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

from utils import processGazeTracking

class GazeTrackingChart(QWidget):
    def __init__(self):
        super(GazeTrackingChart, self).__init__()
        self.status = ['right', 'left', 'blink', 'focus']

        self.series = QPieSeries()
        # Hovering signal
        self.series.hovered.connect(self.__slice_hovered)

        self.setStyleSheet('background-color:white')

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setTitle("Gaze-Tracking Pie Chart")
        self.chart.setTheme(QChart.ChartThemeBlueNcs)
        self.chart.addSeries(self.series)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)

        self.chartview = QChartView(self.chart)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chartview)
        self.setLayout(vbox)


    def addData(self, data):
        status = processGazeTracking(data)

        self.series.clear()
        for state in self.status:
            self.series.append(state, status[state])

        self.__expand_slice()

    def __expand_slice(self):
        slices = self.series.slices()

        idx = 0
        max_slice_val = -1
        for i in range(len(slices)):
            if slices[i].value() > max_slice_val:
                max_slice_val = slices[i].value()
                idx = i

        slices[idx].setExploded(True)
        slices[idx].setLabelVisible(True)
        slices[idx].setPen(QPen(Qt.darkBlue, 2))
        slices[idx].setBrush(Qt.darkBlue)
            
    def __slice_hovered(self, slice):
        slice.setLabelVisible(True)
