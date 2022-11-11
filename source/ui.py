from PyQt6.QtWidgets import QApplication, QGraphicsScene, QSlider, QDockWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import numpy as np
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from grid import Grid
from point import Point
from searcher import Searcher
import env


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, name_gr='q'):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        #fig.suptitle(env.loc[name_gr][env.lang], fontsize=8)
        super(MplCanvas, self).__init__(fig)


class UI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = uic.loadUi("../wdw.ui")
        self.view = self.window.scene
        self.scene = QGraphicsScene()

        self.view.setSceneRect(env.SCENE_LEFT, env.SCENE_BOTTOM, env.SCENE_RIGHT, env.SCENE_TOP)
        self.view.setScene(self.scene)

        self.textSliderEntropy = self.window.textSliderEntropy
        self.textSliderDistribution = self.window.textSliderDistribution
        self.textSliderVariance = self.window.textSliderVariance
        self.textSliderSimSpeed = self.window.textSliderSimSpeed
        self.textSliderParticlesNumber = self.window.textSliderParticlesNumber
        self.textSliderItemsNumber = self.window.textSliderItemsNumber
        self.locButton = self.window.locButton
        self.startButton = self.window.startButton
        self.pauseButton = self.window.pauseButton
        self.speedSlider = self.window.speedSlider
        self.varianceSlider = self.window.varianceSlider
        self.checkBoxSearchSimple = self.window.checkBoxSearchSimple
        self.spinBoxAgentsCount = self.window.spinBoxAgentsCount
        self.spinBoxTargetsCount = self.window.spinBoxTargetsCount
        self.widgetPlotEntropy = self.window.widgetPlotEntropy
        self.widgetPlotDistribution = self.window.widgetPlotDistribution
        self.distributionButton = self.window.distributionButton

        self.x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
        self.y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
        self.grid = Grid(env.SCENE_RIGHT, env.SCENE_TOP, env.GRID_WIDTH, env.GRID_HEIGHT)
        self.point = Point(self.x, self.y, (env.SCENE_LEFT, env.SCENE_RIGHT),
                           (env.SCENE_BOTTOM, env.SCENE_TOP),
                           x_distribution="gaussian_mixture", y_distribution="gaussian_mixture",
                           variance=0,
                           size=env.POINT_SIZE)
        self.searcher = Searcher(self.point, self.grid, self.scene, self)

        self.distributionButton.clicked.connect(self.update_distribution)
        self.locButton.clicked.connect(self.change_loc)
        self.startButton.clicked.connect(self.launch)
        self.pauseButton.clicked.connect(self.pause)
        self.checkBoxSearchSimple.stateChanged.connect(self.searcher.change_search_type)
        self.spinBoxAgentsCount.valueChanged.connect(
            lambda: self.searcher.change_agents_count(self.spinBoxAgentsCount.value()))
        self.spinBoxTargetsCount.valueChanged.connect(
            lambda: self.searcher.change_targets_count(self.spinBoxTargetsCount.value()))

        self.plot_entropy = MplCanvas(self, name_gr='entropy', width=5, height=4, dpi=100)
        self.layout_plot_entropy = QVBoxLayout()
        self.layout_plot_entropy.addWidget(self.plot_entropy)
        self.widgetPlotEntropy.setLayout(self.layout_plot_entropy)
        self.plot_distribution = MplCanvas(self, name_gr='dist', width=5, height=4, dpi=100)
        self.layout_plot_distribution = QVBoxLayout()
        self.layout_plot_distribution.addWidget(self.plot_distribution)
        self.widgetPlotDistribution.setLayout(self.layout_plot_distribution)
        self.speedSlider.valueChanged.connect(self.change_speed)
        self.varianceSlider.valueChanged.connect(self.update_variance)

        self.update_variance()
        self.was_launched = 0
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
        self.was_launched = 1
        self.searcher.restart()
        self.reset_settings()

    def reset_settings(self):
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))
        self.pauseButton.setText(env.loc['pause'][env.lang])
        self.steps = 0
        self.entropy_history = []

    def pause(self):
        if self.was_launched == 0:
            return
        if self.timer.isActive():
            self.real_pause()
        else:
            self.real_resume()

    def real_resume(self):
        self.pauseButton.setText(env.loc['pause'][env.lang])
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def real_pause(self):
        self.pauseButton.setText(env.loc['resume'][env.lang])
        self.timer.stop()

    def change_speed(self):
        env.SPEED_MODIFIER = 0.1 * self.speedSlider.value()
        if self.timer.isActive():
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def update_variance(self):
        x = np.linspace(-20, 20, 100)
        y = self.point.change_distribution(x, variance=self.varianceSlider.value(), change_dist=False)
        self.update_plot(self.plot_distribution, x, y)

    def update_distribution(self):
        x = np.linspace(-20, 20, 100)
        y = self.point.change_distribution(x, variance=self.varianceSlider.value(), change_dist=True)
        self.update_plot(self.plot_distribution, x, y)

    def update_plot(self, plot, x, y):
        plot.axes.cla()
        plot.axes.plot(x, y)
        plot.draw()

    def update_all_labels(self):
        self.textSliderEntropy.setText(env.loc['entropy'][env.lang])
        self.textSliderDistribution.setText(env.loc['dist'][env.lang])
        self.textSliderVariance.setText(env.loc['variance'][env.lang])
        self.distributionButton.setText(env.loc['change_dist'][env.lang])
        self.checkBoxSearchSimple.setText(env.loc['1_axes_search'][env.lang])
        self.textSliderSimSpeed.setText(env.loc['sim_speed'][env.lang])
        self.textSliderParticlesNumber.setText(env.loc['number_of_particles'][env.lang])
        self.textSliderItemsNumber.setText(env.loc['number_of_items'][env.lang])

    def change_loc(self):
        if env.lang == 'ru':
            env.lang = 'en'
        else:
            env.lang = 'ru'
        self.update_all_labels()