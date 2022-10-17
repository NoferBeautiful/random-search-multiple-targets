from PyQt6.QtWidgets import QApplication, QGraphicsScene, QSlider, QDockWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import numpy as np
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from grid import Grid
from point import Point
from searcher import Searcher
import env
from plot import MplCanvas


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
        self.checkBoxSearchSimple = self.window.checkBoxSearchSimple
        self.spinBoxAgentsCount = self.window.spinBoxAgentsCount
        self.spinBoxTargetsCount = self.window.spinBoxTargetsCount

        self.x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
        self.y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
        self.grid = Grid(env.SCENE_RIGHT, env.SCENE_TOP, env.GRID_WIDTH, env.GRID_HEIGHT)
        self.point = Point(self.x, self.y, (env.SCENE_LEFT, env.SCENE_RIGHT),
                           (env.SCENE_BOTTOM, env.SCENE_TOP),
                           x_distribution="normal", y_distribution="normal",
                           sampler_params={"x": [0, 10], "y": [0, 10]},
                           size=env.POINT_SIZE)
        self.searcher = Searcher(self.point, self.grid, self.scene, self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.searcher.search)

        self.startButton.clicked.connect(self.launch)
        self.pauseButton.clicked.connect(self.pause)
        self.speedSlider.valueChanged.connect(self.change_speed)
        self.checkBoxSearchSimple.stateChanged.connect(self.searcher.change_search_type)
        self.spinBoxAgentsCount.valueChanged.connect(lambda : self.searcher.change_agents_count(self.spinBoxAgentsCount.value()))
        self.spinBoxTargetsCount.valueChanged.connect(lambda : self.searcher.change_targets_count(self.spinBoxTargetsCount.value()))

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        #self.window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, sc)

    def start_exe(self):
        self.window.show()
        self.app.exec()

    def launch(self):
        self.scene.clear()
        self.x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
        self.y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
        self.point.restart(self.x, self.y, x_distribution="normal", y_distribution="normal",
                           sampler_params={"x": [0, 10], "y": [0, 10]})
        self.grid.restart()
        self.searcher.restart()
        self.point.appear(self.scene)
        self.grid.draw(self.scene)
        self.point.draw(self.scene)
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

        self.reset_settings()

    def reset_settings(self):
        self.pauseButton.setText('PAUSE')
        self.checkBoxSearchSimple.setChecked(1)

    def pause(self):
        if self.timer.isActive():
            self.pauseButton.setText('RESUME')
            self.timer.stop()
        else:
            self.pauseButton.setText('PAUSE')
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def change_speed(self):
        env.SPEED_MODIFIER = 0.1 * self.speedSlider.value()
        if self.timer.isActive():
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))
