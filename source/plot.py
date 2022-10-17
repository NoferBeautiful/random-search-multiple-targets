import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Plot():
    def __init__(self, tick=0.5):
        self.timerUpdate = QTimer()
        self.timerUpdate.setInterval(tick)
        self.timerUpdate.timeout.connect(self.draw)

    def start(self):
        self.timerUpdate.start()

    def draw(self):
        pass