import numpy as np
from PyQt6.QtGui import QPen, QBrush
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
        self.__width = width
        self.__height = height
        self.__n = n
        self.__m = m
        self.__n_targets = 1
        self.__found_targets = np.zeros(self.__n_targets, dtype=int)
        self.__x_target = np.random.randint(0, self.__n, size=self.__n_targets)
        self.__y_target = np.random.randint(0, self.__m, size=self.__n_targets)
        self.__is_visited = np.zeros((n, m), dtype=int)
        self.__pen_grid = QPen(Qt.GlobalColor.gray, 0.5)
        self.__target_brush = QBrush(Qt.GlobalColor.green)
        self.__visited_brush = QBrush(Qt.GlobalColor.gray)
        self.__visited_target = QBrush(Qt.GlobalColor.darkGreen)

    def update_targets_count(self, n):
        self.__n_targets = n

    def restart(self):
        self.__x_target = np.random.randint(0, self.__n, size=self.__n_targets)
        self.__y_target = np.random.randint(0, self.__m, size=self.__n_targets)
        self.__found_targets = np.zeros(self.__n_targets, dtype=int)
        self.__is_visited = np.zeros((self.__n, self.__m), dtype=int)

    def where_point(self, x, y):
        """
        Returns position of given dot in the grid
        :param x: x coordinate
        :param y: y coordinate
        """
        return int(x / self.__x_delta), int(y / self.__y_delta)

    def get_entropy(self):
        return (self.__n_targets - self.__found_targets.sum()) * \
               -np.log((1 + (self.__is_visited == 1).sum()) / np.prod(self.__is_visited.shape))

    def check(self, x, y, canvas):
        """
        Marks cell where point is as visited and checks if target is found
        :param x: x coordinate
        :param y: y coordinate
        :param canvas:
        :return: 0 if no coordinate of target is found, 1 if only x coordinate if found, 2 if only y
        coordinate is found, 3 if target is found
        """
        i, j = self.where_point(x, y)
        if i < self.__n and j < self.__m and self.__is_visited[i][j] == 0:
            self.__is_visited[i][j] = 1
            canvas.addRect(i * self.__x_delta,
                           j * self.__y_delta,
                           self.__x_delta, self.__y_delta,
                           self.__pen_grid, self.__visited_brush)
        if self.__n_targets > 1:
            for k in range(self.__n_targets):
                if i == self.__x_target[k] and j == self.__y_target[k]:
                    self.__found_targets[k] = 1
                    canvas.addRect(i * self.__x_delta,
                                   j * self.__y_delta,
                                   self.__x_delta, self.__y_delta,
                                   self.__pen_grid, self.__visited_target)
            if self.__found_targets.sum() != self.__n_targets:
                return 0, 0
            return 3, 0
        else:
            if i != self.__x_target[0] and j != self.__y_target[0]:
                return 0, 0
            elif j != self.__y_target[0]:
                return 1, i * self.__x_delta + self.__x_delta / 2
            elif i != self.__x_target[0]:
                return 2, j * self.__y_delta + self.__y_delta / 2
            return 3, 0

    def draw(self, canvas):
        x_start = 0
        for _ in range(self.__n):
            canvas.addLine(x_start, 0, x_start, self.__height, self.__pen_grid)
            x_start += self.__x_delta
        y_start = 0
        for _ in range(self.__m):
            canvas.addLine(0, y_start, self.__width, y_start, self.__pen_grid)
            y_start += self.__y_delta
        for k in range(self.__n_targets):
            canvas.addRect(self.__x_target[k] * self.__x_delta,
                           self.__y_target[k] * self.__y_delta,
                           self.__x_delta, self.__y_delta,
                           self.__pen_grid, self.__target_brush)
