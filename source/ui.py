from PyQt6.QtWidgets import QApplication, QGraphicsScene, QVBoxLayout, QMainWindow
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import numpy as np

from os import startfile
import sys
from subprocess import call

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter

from grid import Grid
from point import Point
from searcher import Searcher
import env


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, name_gr='q'):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # fig.suptitle(env.loc[name_gr][env.lang], fontsize=8)
        super(MplCanvas, self).__init__(fig)


from source.wdw import Ui_MainWindow


class UI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = Ui_MainWindow()    #uic.loadUi("../wdw.ui")
        self.__window = QMainWindow()
        self.window.setupUi(self.__window)
        self.view = self.window.scene
        self.scene = QGraphicsScene()

        self.backButton = self.window.backButton
        self.backButton.clicked.connect(lambda: self.show_only_chosen_section(self.ui_main))

        # Main menu
        self.labelMainYear = self.window.labelMainYear
        self.labelMainVmk = self.window.labelMainVmk
        self.labelMainFizfak = self.window.labelMainFizfak
        self.menuButtonDemo = self.window.menuButtonDemo
        self.menuButtonTheory = self.window.menuButtonTheory
        self.menuButtonAuthors = self.window.menuButtonAuthors
        self.menuButtonExit = self.window.menuButtonExit
        self.labelMainString1 = self.window.labelMainString1
        self.labelMainString2 = self.window.labelMainString2
        self.labelMainString3 = self.window.labelMainString3
        self.labelMainString4 = self.window.labelMainString4
        self.labelMainString5 = self.window.labelMainString5
        self.ui_main = [self.menuButtonDemo,
                        self.menuButtonTheory,
                        self.menuButtonAuthors,
                        self.menuButtonExit,
                        self.labelMainVmk,
                        self.labelMainFizfak,
                        self.labelMainYear,
                        self.labelMainString1,
                        self.labelMainString2,
                        self.labelMainString3,
                        self.labelMainString4,
                        self.labelMainString5]

        self.menuButtonDemo.clicked.connect(lambda: self.show_only_chosen_section(self.ui_demo))
        self.menuButtonTheory.clicked.connect(self.theory)
        self.menuButtonAuthors.clicked.connect(lambda: self.show_only_chosen_section(self.ui_authors))
        self.menuButtonExit.clicked.connect(lambda: sys.exit(0))

        # Authors
        self.labelAuthorsDima = self.window.labelAuthorsDima
        self.labelAuthorsNikita = self.window.labelAuthorsNikita
        self.labelAuthorsDimaText = self.window.labelAuthorsDimaText
        self.labelAuthorsNikitaText = self.window.labelAuthorsNikitaText
        self.labelAuthorsLector = self.window.labelAuthorsLector
        self.labelAuthorsSeminarist = self.window.labelAuthorsSeminarist

        self.ui_authors = [self.labelAuthorsDima,
                           self.labelAuthorsNikita,
                           self.labelAuthorsDimaText,
                           self.labelAuthorsNikitaText,
                           self.labelAuthorsLector,
                           self.labelAuthorsSeminarist]

        # Demonstration
        self.view.setSceneRect(env.SCENE_LEFT, env.SCENE_BOTTOM, env.SCENE_RIGHT, env.SCENE_TOP)
        self.view.setScene(self.scene)

        self.textSliderEntropy = self.window.textSliderEntropy
        self.textSliderDistribution = self.window.textSliderDistribution
        self.textSliderVariance = self.window.textSliderVariance
        self.textSliderSimSpeed = self.window.textSliderSimSpeed
        self.textSliderSize = self.window.textSliderSize
        self.textSliderParticlesNumber = self.window.textSliderParticlesNumber
        self.textSliderItemsNumber = self.window.textSliderItemsNumber
        self.textSliderPeak = self.window.textSliderPeak
        self.locButton = self.window.locButton
        self.startButton = self.window.startButton
        self.pauseButton = self.window.pauseButton
        self.speedSlider = self.window.speedSlider
        self.sizeSlider = self.window.sizeSlider
        self.varianceSlider = self.window.varianceSlider
        self.peakSlider = self.window.peakSlider
        self.checkBoxSearchSimple = self.window.checkBoxSearchSimple
        self.spinBoxAgentsCount = self.window.spinBoxAgentsCount
        self.spinBoxTargetsCount = self.window.spinBoxTargetsCount
        self.widgetPlotEntropy = self.window.widgetPlotEntropy
        self.widgetPlotDistribution = self.window.widgetPlotDistribution
        self.distributionButton = self.window.distributionButton
        self.ui_demo = [self.view,
                        self.textSliderEntropy,
                        self.textSliderDistribution,
                        self.textSliderVariance,
                        self.textSliderSimSpeed,
                        self.textSliderSize,
                        self.textSliderParticlesNumber,
                        self.textSliderItemsNumber,
                        self.textSliderPeak,
                        self.locButton,
                        self.startButton,
                        self.pauseButton,
                        self.speedSlider,
                        self.sizeSlider,
                        self.varianceSlider,
                        self.peakSlider,
                        self.checkBoxSearchSimple,
                        self.spinBoxAgentsCount,
                        self.spinBoxTargetsCount,
                        self.widgetPlotEntropy,
                        self.widgetPlotDistribution,
                        self.distributionButton]

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
        self.checkBoxSearchSimple.stateChanged.connect(lambda: self.searcher.change_search_type())
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
        self.sizeSlider.valueChanged.connect(self.change_size)
        self.varianceSlider.valueChanged.connect(self.update_variance)
        self.peakSlider.valueChanged.connect(self.update_peak)

        self.update_variance()
        self.may_be_paused = 0
        self.was_launched = 0
        self.steps = 0
        self.entropy_history = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # kys if you see this shitcoding
        self.change_loc()
        self.change_loc()
        self.locButton.hide()
        self.locButton.show()
        # end of shitcoding part

        self.uis = [self.ui_main, self.ui_demo, self.ui_authors]

        self.show_only_chosen_section(self.ui_main)

    def hide_section(self, section):
        for i in section:
            i.hide()

    def show_section(self, section):
        for i in section:
            i.show()

    def show_only_chosen_section(self, section):
        for i in self.uis:
            if i != section:
                self.hide_section(i)
        self.show_section(section)

        if section == self.ui_main:
            self.backButton.hide()
        else:
            self.backButton.show()

        if section == self.ui_authors:
            self.labelMainString1.show()
            self.labelMainString2.show()

    def step(self):
        self.steps += 1
        if self.steps < 3:
            return
        self.entropy_history.append(self.grid.get_entropy())
        if len(self.entropy_history) > 3000:
            del self.entropy_history[-3001::-1]
        self.searcher.search()
        if self.steps % 100 == 0:
            self.update_plot(self.plot_entropy, range(self.steps - len(self.entropy_history) + 1, self.steps + 1),
                             self.entropy_history)

    def start_exe(self):
        self.__window.show()
        self.app.exec()

    def launch(self):
        self.grid = Grid(env.SCENE_RIGHT, env.SCENE_TOP, env.GRID_WIDTH, env.GRID_HEIGHT)
        self.searcher = Searcher(self.point, self.grid, self.scene, self)
        self.searcher.change_agents_count(self.spinBoxAgentsCount.value())
        self.searcher.change_targets_count(self.spinBoxTargetsCount.value())
        self.may_be_paused = 1
        self.searcher.restart()
        #self.reset_settings() ###########################
        self.was_launched = 1

    def reset_settings(self):
        self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))
        self.pauseButton.setText(env.loc['pause'][env.lang])
        self.steps = 0
        self.may_be_paused = 1
        self.entropy_history = []
        self.update_plot(self.plot_entropy)
        self.update_distribution()
        self.update_distribution()
        if self.searcher.agents > 1:
            self.checkBoxSearchSimple.setChecked(False)

    def pause(self):
        if self.may_be_paused == 0:
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
        env.SPEED_MODIFIER = 0.1 * (8 + self.speedSlider.value())
        if self.timer.isActive():
            self.timer.start(int(env.SPEED_BASE / env.SPEED_MODIFIER))

    def update_variance(self):
        x = np.linspace(-20, 20, 100)
        y = self.searcher.change_distribution(x, variance=self.varianceSlider.value(), change_dist=False)
        self.update_plot(self.plot_distribution, x, y)

    def update_peak(self):
        x = np.linspace(-20, 20, 100)
        y = self.searcher.change_distribution(x, variance=self.varianceSlider.value(),
                                              p1=self.peakSlider.value() / 100,
                                              change_dist=False)
        self.update_plot(self.plot_distribution, x, y)

    def update_distribution(self):
        x = np.linspace(-20, 20, 100)
        y = self.searcher.change_distribution(x, variance=self.varianceSlider.value(), change_dist=True)
        self.update_plot(self.plot_distribution, x, y)

    def change_size(self):
        env.GRID_HEIGHT = env.GRID_WIDTH = self.sizeSlider.value()
        if self.was_launched:
            self.launch()

    def update_plot(self, plot, x=[], y=[]):
        plot.axes.cla()
        if len(y) > 0:
            plot.axes.set_yticks([min(y), max(y)])
        plot.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plot.axes.plot(x, y)
        plot.draw()

    def update_all_labels(self):
        self.textSliderEntropy.setText(env.loc['entropy'][env.lang])
        self.textSliderDistribution.setText(env.loc['dist'][env.lang])
        self.textSliderVariance.setText(env.loc['variance'][env.lang])
        self.textSliderPeak.setText(env.loc['peak'][env.lang])
        self.distributionButton.setText(env.loc['change_dist'][env.lang])
        self.checkBoxSearchSimple.setText(env.loc['1_axes_search'][env.lang])
        self.textSliderSimSpeed.setText(env.loc['sim_speed'][env.lang])
        self.textSliderParticlesNumber.setText(env.loc['number_of_particles'][env.lang])
        self.textSliderItemsNumber.setText(env.loc['number_of_items'][env.lang])
        self.textSliderSize.setText(env.loc['size_field'][env.lang])
        self.menuButtonDemo.setText(env.loc['button_demo'][env.lang])
        self.menuButtonTheory.setText(env.loc['button_theory'][env.lang])
        self.menuButtonAuthors.setText(env.loc['button_authors'][env.lang])
        self.menuButtonExit.setText(env.loc['button_exit'][env.lang])

        self.backButton.setText(env.loc['back'][env.lang])
        self.startButton.setText(env.loc['start'][env.lang])
        # self.startButton.setTextFormat(self.startButton.TextFormat())
        if self.pauseButton.text() in env.loc['resume'].values():
            self.pauseButton.setText(env.loc['resume'][env.lang])
        elif self.pauseButton.text() in env.loc['pause'].values():
            self.pauseButton.setText(env.loc['pause'][env.lang])

        need_to_change_bold = [self.textSliderEntropy,
                               self.textSliderDistribution,
                               self.textSliderVariance,
                               self.textSliderSimSpeed,
                               self.textSliderParticlesNumber,
                               self.textSliderItemsNumber,
                               self.textSliderSize,
                               self.textSliderPeak,
                               self.distributionButton,
                               self.checkBoxSearchSimple,
                               self.backButton,
                               self.locButton,
                               self.menuButtonDemo,
                               self.menuButtonTheory,
                               self.menuButtonAuthors,
                               self.menuButtonExit]
        font = QFont('MS Shell Dlg 2', 16)
        for item in need_to_change_bold:
            if item == self.textSliderDistribution:
                item.setFont(QFont('MS Shell Dlg 2', 12))
            else:
                item.setFont(font)
            item.setStyleSheet("font-weight: bold")

        need_to_change_alignment = [self.textSliderEntropy,
                                    self.textSliderDistribution,
                                    self.textSliderVariance,
                                    self.textSliderSimSpeed,
                                    self.textSliderParticlesNumber,
                                    self.textSliderItemsNumber,
                                    self.textSliderSize,
                                    self.textSliderPeak]
        for item in need_to_change_alignment:
            item.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def change_loc(self):
        if env.lang == 'ru':
            env.lang = 'en'
        else:
            env.lang = 'ru'
        self.update_all_labels()

    def open_file(self, filename):
        if sys.platform == "win32":
            startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            call([opener, filename])

    def theory(self):
        self.open_file('statphys_theory.pdf')
