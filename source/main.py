from PyQt6.QtWidgets import QApplication, QGraphicsScene
from PyQt6 import uic
from PyQt6.QtCore import QTimer
import sys
import numpy as np

from grid import Grid
from point import Point
import env


class Searcher:
    def __init__(self, point, grid, scene):
        self.__point = point
        self.__grid = grid
        self.__scene = scene
        self.__found_x = False
        self.__found_y = False

    def end(self):
        exit(0)

    def search(self):
        point.move()
        check = grid.check(*point.get_point(), self.__scene)
        if check == 3:
            self.end()
        elif check == 2 and not self.__found_y:
            point.change_y_distribution("end")
            self.__found_y = True
        elif check == 3 and not self.__found_x:
            point.change_x_distribution("end")
            self.__found_x = True


app = QApplication(sys.argv)
window = uic.loadUi("../wdw.ui")

view = window.scene

startButton = window.startButton

scene = QGraphicsScene()

grid = Grid(env.SCENE_RIGHT, env.SCENE_TOP, env.GRID_WIDTH, env.GRID_HEIGHT)
x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
point = Point(x, y, (env.SCENE_LEFT, env.SCENE_RIGHT),
              (env.SCENE_BOTTOM, env.SCENE_TOP),
              x_distribution="normal", y_distribution="normal",
              sampler_params={"x": [0, 10], "y": [0, 10]},
              size=env.POINT_SIZE)

point.appear(scene)
grid.draw(scene)
point.draw(scene)

searcher = Searcher(point, grid, scene)

view.setSceneRect(env.SCENE_LEFT, env.SCENE_BOTTOM, env.SCENE_RIGHT, env.SCENE_TOP)
view.setScene(scene)

timer = QTimer()
timer.timeout.connect(searcher.search)
timer.start(10)

window.show()

app.exec()
