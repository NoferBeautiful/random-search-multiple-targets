import numpy as np
import env
from point import Point


class Searcher:
    def __init__(self, point, grid, scene, UI):
        self.__points = [point]
        self.__grid = grid
        self.__scene = scene
        self.__found_x = False
        self.__found_y = False
        self.__UI = UI
        self.__searchFull = 1
        self.__agents = 1

    def restart(self):
        self.__UI.reset_settings()
        self.__scene.clear()
        self.__found_x = False
        self.__found_y = False
        self.__grid.restart()
        self.__grid.draw(self.__scene)
        for point in self.__points:
            x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
            y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
            point.restart(x, y, x_distribution="normal", y_distribution="normal",
                          sampler_params={"x": [0, 10], "y": [0, 10]})
            point.appear(self.__scene)
            point.draw(self.__scene)

    def end(self):
        self.__UI.real_pause()

    def change_search_type(self):
        if self.__searchFull:
            self.__searchFull = 0
        else:
            self.__searchFull = 1
        self.restart()

    def change_agents_count(self, n):
        self.__UI.real_pause()
        self.__agents = n
        self.__points = []
        for i in range(self.__agents):
            x = np.random.randint(env.SCENE_LEFT, env.SCENE_RIGHT)
            y = np.random.randint(env.SCENE_BOTTOM, env.SCENE_TOP)
            self.__points.append(Point(x, y, (env.SCENE_LEFT, env.SCENE_RIGHT),
                                       (env.SCENE_BOTTOM, env.SCENE_TOP),
                                       x_distribution="normal", y_distribution="normal",
                                       sampler_params={"x": [0, 10], "y": [0, 10]},
                                       size=env.POINT_SIZE))
        self.restart()
        self.__UI.real_resume()

    def change_targets_count(self, n):
        if n > 1:
            pass
        self.__UI.real_pause()
        self.__grid.update_targets_count(n)
        self.restart()
        self.__UI.real_resume()

    def search(self):
        for point in self.__points:
            point.move()
            check = self.__grid.check(*point.get_point(), self.__scene)
            if check == 3:
                self.end()
            elif not self.__searchFull:
                if check == 2:
                    point.change_y_distribution("end")
                elif check == 1:
                    point.change_x_distribution("end")
