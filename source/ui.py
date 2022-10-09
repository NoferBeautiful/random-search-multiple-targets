from PyQt6.QtWidgets import QApplication, QGraphicsScene, QSlider
from PyQt6.QtCore import QTimer
from PyQt6 import uic
import numpy as np
import sys

from grid import Grid
from point import Point
import env


class UI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = uic.loadUi("../wdw.ui")
        self.view = self.window.scene
        self.scene = QGraphicsScene()

        self.view.setSceneRect(env.SCENE_LEFT, env.SCENE_BOTTOM, env.SCENE_RIGHT, env.SCENE_TOP)
        self.view.setScene(self.scene)

        self.startButton = self.window.startButton
        self.pauseButton = self.window.pauseButton
        self.speedSlider = self.window.speedSlider

        self.startButton.clicked.connect(self.launch)
        self.pauseButton.clicked.connect(self.pause)
        self.speedSlider.valueChanged.connect(self.change_speed)

        self.x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
        self.y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
        self.grid = Grid(env.SCENE_RIGHT, env.SCENE_TOP, env.GRID_WIDTH, env.GRID_HEIGHT)
        self.point = Point(self.x, self.y, (env.SCENE_LEFT, env.SCENE_RIGHT),
                      (env.SCENE_BOTTOM, env.SCENE_TOP),
                      x_distribution="normal", y_distribution="normal",
                      sampler_params={"x": [0, 10], "y": [0, 10]},
                      size=env.POINT_SIZE)

        self.timer = QTimer()

    def start_exe(self):
        self.window.show()
        self.app.exec()

    def launch(self):
        self.scene.clear() #добавить restart
        self.point.appear(self.scene)
        self.grid.draw(self.scene)
        self.point.draw(self.scene)
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def change_speed(self):
        env.SPEED_MODIFIER = 0.1 * self.speedSlider.value()
        if self.timer.isActive():
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))