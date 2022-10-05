import numpy as np
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt

class Grid:
    def __init__(self, width, height, n, m):
        """
        Grid initialization
        :param width: width of the grid
        :param height: height of the grid
        :param n: amount of columns in the grid
        :param m: amount of rows in the grid
        """
        self.__x_grid = np.linspace(0, width, n)
        self.__y_grid = np.linspace(0, height, m)
        self.__x_delta = width / n
        self.__y_delta = height / m
        self.__x_target = np.random.randint(0, n)
        self.__y_target = np.random.randint(0, m)
        self.__is_visited = np.zeros((n, m), dtype=int)
        self.__pen_grid = QPen(Qt.GlobalColor.gray, 2)

    def where_point(self, x, y):
        """
        Returns position of given dot in the grid
        :param x: x coordinate
        :param y: y coordinate
        """
        return 0, 0#int(x / self.__x_delta), int(y / self.__y_delta)

    def check(self, x, y):
        """
        Marks cell where point is as visited and checks if target is found
        :param x: x coordinate
        :param y: y coordinate
        :return: 0 if no coordinate of target is found, 1 if only x coordinate if found, 2 if only y
        coordinate is found, 3 if target is found
        """
        i, j = self.where_point(x, y)
        self.__is_visited[i][j] = 1
        if i != self.__x_target and j != self.__y_target:
            return 0
        elif j != self.__y_target:
            return 1
        elif i != self.__x_target:
            return 2
        return 3

    def draw(self, canvas):
        for i in self.__x_grid:
            canvas.addLine(i, 0, i, 500, self.__pen_grid)
        for i in self.__y_grid:
            canvas.addLine(0, i, 500, i, self.__pen_grid)
