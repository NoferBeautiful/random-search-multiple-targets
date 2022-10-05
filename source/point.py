import numpy as np
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtCore import Qt

from sampling import DotSampler


class Point:
    def __init__(self, x=0, y=0, color='b', sampler=DotSampler(),
                 x_distribution="normal", y_distribution="normal",
                 sampler_params=None, speed=10, size=25):
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

    def appear(self, canvas):
        """
        Places point on screen
        :param canvas:
        :return:
        """
        self.ell = canvas.addEllipse(*(self.get_point()), self.__size,
                                self.__size, self.__pen, self.__brush)
        self.ell.ItemIsMovable = 1

    def draw(self, canvas):
        """
        Draws dot at given canvas
        :param canvas:
        :return:
        """
        #canvas.addItem(QGraphicsItem())

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
                                                      self.__sampler_params)
            self.__n_iter = max(np.max(np.ceil(self.__delta / self.__speed)), 1)
            self.__delta /= self.__n_iter
            self.__point += self.__delta
            self.__i = 1
        self.ell.moveBy(*(self.__delta))