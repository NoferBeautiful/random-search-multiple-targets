import numpy as np
from sampling import DotSampler


class Point:
    def __init__(self, x=0, y=0, color='b', sampler=DotSampler(),
                 x_distribution="normal", y_distribution="normal",
                 sampler_params=None, n_iter=10):
        """
        Point initialization
        :param x: x coordinate
        :param y: y coordinate
        :param color: color of the point
        """
        self.__point = np.array([x, y], dtype=np.float64)
        self.__color = color
        self.__sampler = sampler
        self.__sampler_params = sampler_params
        self.__n_iter = n_iter
        self.__x_distribution = x_distribution
        self.__y_distribution = y_distribution
        self.__i = 0
        self.__to_generate = True
        self.__delta = np.zeros(2, dtype=np.float64)

    def draw(self, canvas):
        """
        Draws dot at given canvas
        :param canvas:
        :return:
        """
        pass

    def get_point(self):
        """
        :return: point coords
        """
        return self.__point[0], self.__point[1]

    def change_x_distribution(self, new_x="end"):
        self.__x_distribution = new_x

    def change_y_distribution(self, new_y="end"):
        self.__y_distribution = new_y

    def move(self):
        """
        Moves dot to random direction
        :return:
        """
        if self.__i < self.__n_iter:
            self.__point += self.__delta
            self.__i += 1
        else:
            self.__delta = self.__sampler.sample_from(self.__x_distribution,
                                                      self.__y_distribution,
                                                      self.__sampler_params) / self.__n_iter
            self.__point += self.__delta
            self.__i = 1
