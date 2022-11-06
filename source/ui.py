from PyQt6.QtWidgets import QApplication, QGraphicsScene, QSlider, QDockWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import numpy as np
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from grid import Grid
from point import Point
from searcher import Searcher
import env


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.
        super(MplCanvas, self).__init__(fig)


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
        self.widgetPlotEntropy = self.window.widgetPlotEntropy

        self.x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
        self.y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
        self.grid = Grid(env.SCENE_RIGHT, env.SCENE_TOP, env.GRID_WIDTH, env.GRID_HEIGHT)
        self.point = Point(self.x, self.y, (env.SCENE_LEFT, env.SCENE_RIGHT),
                           (env.SCENE_BOTTOM, env.SCENE_TOP),
                           x_distribution="normal", y_distribution="normal",
                           sampler_params={"x": [0, 10], "y": [0, 10]},
                           size=env.POINT_SIZE)
        self.searcher = Searcher(self.point, self.grid, self.scene, self)

        self.startButton.clicked.connect(self.launch)
        self.pauseButton.clicked.connect(self.pause)
        self.speedSlider.valueChanged.connect(self.change_speed)
        self.checkBoxSearchSimple.stateChanged.connect(self.searcher.change_search_type)
        self.spinBoxAgentsCount.valueChanged.connect(
            lambda: self.searcher.change_agents_count(self.spinBoxAgentsCount.value()))
        self.spinBoxTargetsCount.valueChanged.connect(
            lambda: self.searcher.change_targets_count(self.spinBoxTargetsCount.value()))

        self.plot_entropy = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout_plot_entropy = QVBoxLayout()
        self.layout_plot_entropy.addWidget(self.plot_entropy)
        self.widgetPlotEntropy.setLayout(self.layout_plot_entropy)

        self.steps = 0
        self.entropy_history = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

    def step(self):
        self.steps += 1
        if self.steps < 3:
            return
        self.entropy_history.append(self.grid.get_entropy())
        self.searcher.search()
        if self.steps % 100 == 0:
            self.update_plot(self.plot_entropy, range(3, self.steps + 1), self.entropy_history)

    def start_exe(self):
        self.window.show()
        self.app.exec()

    def launch(self):
        self.searcher.restart()
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))
        self.reset_settings()

    def reset_settings(self):
        self.pauseButton.setText('PAUSE')
        self.steps = 0
        self.entropy_history = []
        self.checkBoxSearchSimple.setChecked(1)

    def pause(self):
        if self.timer.isActive():
            self.pauseButton.setText('RESUME')
            self.timer.stop()
        else:
            self.pauseButton.setText('PAUSE')
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def real_resume(self):
        self.pauseButton.setText('PAUSE')
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def real_pause(self):
        self.pauseButton.setText('RESUME')
        self.timer.stop()

    def change_speed(self):
        env.SPEED_MODIFIER = 0.1 * self.speedSlider.value()
        if self.timer.isActive():
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def update_plot(self, plot, x, y):
        plot.axes.cla()
        plot.axes.plot(x, y)
        plot.draw()
