import numpy as np
import env
from point import Point
from sampling import distribution_plot


class Searcher:
    def __init__(self, point, grid, scene, UI):
        self.__points = [point]
        self.__grid = grid
        self.__scene = scene
        self.__found_x = False
        self.__found_y = False
        self.__UI = UI
        self.__searchFull = 1
        self.agents = 1
        self.__UI.checkBoxSearchSimple.blockSignals(True)
        self.__UI.checkBoxSearchSimple.setChecked(self.__searchFull == 0)
        self.__UI.checkBoxSearchSimple.blockSignals(False)

    def restart(self):
        self.__UI.was_launched = 1
        self.__UI.reset_settings()
        self.__scene.clear()
        self.__found_x = False
        self.__found_y = False
        self.__grid.restart()
        self.__grid.draw(self.__scene)
        params = self.__points[0].get_params()
        for point in self.__points:
            x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
            y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
            point.restart(x, y, x_distribution=params[0], y_distribution=params[1],
                          sampler_variance=params[2], p1=params[3])
            point.appear(self.__scene)
            point.draw(self.__scene)
        self.__UI.checkBoxSearchSimple.blockSignals(True)
        self.__UI.checkBoxSearchSimple.setChecked(self.__searchFull == 0)
        self.__UI.checkBoxSearchSimple.blockSignals(False)

    def end(self):
        self.__UI.may_be_paused = 0
        self.__UI.real_pause()

    def change_search_type(self):
        if self.__searchFull:
            self.__searchFull = 0
        else:
            self.__searchFull = 1
        self.restart()

    def change_agents_count(self, n):
        self.__UI.real_pause()
        self.agents = n
        params = self.__points[0].get_params()
        self.__points = []
        for i in range(self.agents):
            x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
            y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
            self.__points.append(Point(x, y, (env.SCENE_LEFT, env.SCENE_RIGHT),
                                       (env.SCENE_BOTTOM, env.SCENE_TOP),
                                       x_distribution=params[0], y_distribution=params[1],
                                       variance=params[2], p1=params[3],
                                       size=env.POINT_SIZE))
        self.restart()
        self.__UI.real_resume()

    def change_targets_count(self, n):
        if n > 1:
            self.__searchFull = 1
        self.__UI.real_pause()
        self.__grid.update_targets_count(n)
        self.restart()
        self.__UI.real_resume()

    def search(self):
        for point in self.__points:
            point.move()
            check, new_pos = self.__grid.check(*point.get_point(), self.__scene)
            if check == 3:
                self.end()
            elif not self.__searchFull:
                if check == 2:
                    point.change_y_distribution("end", new_pos=new_pos)
                elif check == 1:
                    point.change_x_distribution("end", new_pos=new_pos)

    def change_distribution(self, x, new_x="end", variance=0, new_pos=None, change_dist=1, p1=1/7):
        for point in self.__points:
            point.change_distribution(x, new_x, variance, new_pos, change_dist, p1)
        return distribution_plot(x, self.__points[0]._Point__x_distribution, variance, p1)
