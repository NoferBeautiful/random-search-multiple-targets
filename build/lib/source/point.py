import numpy as np
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtCore import Qt

from sampling import DotSampler


class Point:
    def __init__(self, x, y, x_limits, y_limits, color='b', sampler=DotSampler(),
                 x_distribution="normal", y_distribution="normal",
                 sampler_params=None, speed=1, size=25):
        """
        Point initialization
        :param x: x coordinate
        :param y: y coordinate
        :param color: color of the point
        """
        self.__point = np.array([x, y], dtype=np.float64)
        delta = 1.1 * size
        self.__x_limits = (x_limits[0] + delta, x_limits[1] - delta)
        self.__y_limits = (y_limits[0] + delta, y_limits[1] - delta)
        self.__color = color
        self.__sampler = sampler
        self.__sampler_params = sampler_params
        self.__speed = speed
        self.__x_distribution = x_distribution
        self.__y_distribution = y_distribution
        self.__i = 0
        self.__to_generate = True
        self.__delta = np.zeros(2, dtype=np.float64)
        self.__size = size
        self.__pen = QPen(Qt.GlobalColor.red, 3)
        self.__brush = QBrush(Qt.GlobalColor.red)
        self.__n_iter = -1
        self.ell = None
        self.__generated = None
        self.__is_generated = None

    def restart(self, x, y, x_distribution, y_distribution, sampler_params):
        self.__point = np.array([x, y], dtype=np.float64)
        self.__sampler_params = sampler_params
        self.__x_distribution = x_distribution
        self.__y_distribution = y_distribution

    def appear(self, canvas):
        """
        Places point on screen
        :param canvas:
        :return:
        """
        self.ell = canvas.addEllipse(*(self.get_point()), self.__size,
                                     self.__size, self.__pen, self.__brush)
        self.ell.ItemIsMovable = True
        self.ell.IsSelectable = True
        self.ell.setZValue(1)

    def draw(self, canvas):
        """
        Draws dot at given canvas
        :param canvas:
        :return:
        """
        # canvas.addItem(QGraphicsItem())

    def get_point(self):
        """
        :return: point coords
        """
        return self.__point[0], self.__point[1]

    def get_generated(self):
        if self.__is_generated:
            return self.__generated
        return None

    def change_x_distribution(self, new_x="end", params=None):
        self.__delta[0] = 0
        self.__x_distribution = new_x

    def change_y_distribution(self, new_y="end", params=None):
        self.__delta[1] = 0
        self.__y_distribution = new_y

    def update_position(self):
        new_pos = self.__point + self.__delta
        if new_pos[0] >= self.__x_limits[1] or new_pos[0] < self.__x_limits[0]:
            self.__delta[0] *= -1
        if new_pos[1] >= self.__y_limits[1] or new_pos[1] < self.__y_limits[0]:
            self.__delta[1] *= -1
        self.__point += self.__delta
        self.__i += 1

    def move(self):
        """
        Moves dot to random direction
        :return:
        """
        if self.__i < self.__n_iter:
            self.update_position()
            self.__is_generated = False
        else:
            self.__is_generated = True
            self.__generated = self.__sampler.sample_from(self.__x_distribution,
                                                          self.__y_distribution,
                                                          self.__sampler_params)
            self.__n_iter = max(np.max(np.ceil(np.abs(self.__generated) / self.__speed)), 1)
            self.__delta = self.__generated / self.__n_iter
            self.__i = 0
            self.update_position()
        self.ell.moveBy(*self.__delta)
