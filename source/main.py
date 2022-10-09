from PyQt6.QtWidgets import QApplication, QGraphicsScene, QSlider
from PyQt6 import uic
from PyQt6.QtCore import QTimer
import sys
import numpy as np

from grid import Grid
from point import Point
from ui import UI
import env


class Searcher:
    def __init__(self, point, grid, scene):
        self.__point = point
        self.__grid = grid
        self.__scene = scene
        self.__found_x = False
        self.__found_y = False

    def end(self):
        UI.pause()

    def search(self):
        self.__point.move()
        check = UI.grid.check(*UI.point.get_point(), self.__scene)
        if check == 3:
            self.end()
        elif check == 2 and not self.__found_y:
            self.__point.change_y_distribution("end")
            self.__found_y = True
        elif check == 3 and not self.__found_x:
            self.__point.change_x_distribution("end")
            self.__found_x = True


UI = UI()
searcher = Searcher(UI.point, UI.grid, UI.scene)
UI.timer.timeout.connect(searcher.search)



UI.start_exe()
