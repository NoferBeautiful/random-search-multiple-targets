class Point:
    def __init__(self, x=0, y=0, color='b'):
        """
        :param x: x coordinate
        :param y: y coordinate
        :param color: color of the point
        """
        self.__x = x
        self.__y = y
        self.__color = color

    def draw_dot(self, canvas):
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
        return self.__x, self.__y

    def move_dot(self, to_x, to_y, n_iter):
        """
        Moves from current position to new position in n_iter iterations
        :param to_x:
        :param to_y:
        :param n_iter:
        :return:
        """
        x_delta = (to_x - self.__x) / n_iter
        y_delta = (to_y - self.__y) / n_iter
        for i in range(n_iter):
            self.__x += x_delta
            self.__y += y_delta
            yield