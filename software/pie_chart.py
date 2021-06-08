from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries

from utils import processGazeTracking

class GazeTrackingChart(QWidget):
    def __init__(self):
        super(GazeTrackingChart, self).__init__()
        self.status = ['right', 'left', 'blink', 'focus']

        self.series = QPieSeries()

        self.setStyleSheet('background-color:white')

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setTitle("Gaze-Tracking Pie Chart")
        self.chart.setTheme(QChart.ChartThemeBrownSand)
        self.chart.addSeries(self.series)

        self.chartview = QChartView(self.chart)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chartview)
        self.setLayout(vbox)

    def addData(self, data):
        status = processGazeTracking(data)

        self.series.clear()
        for state in self.status:
            self.series.append(state, status[state])