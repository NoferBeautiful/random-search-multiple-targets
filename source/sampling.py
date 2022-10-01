import numpy as np


class DotSampler:
    def __init__(self, x_seed=None, y_seed=None):
        """
        DotSampler initialization
        :param x_seed: random generator seed for x-axis
        :param y_seed: random generator seed for y-axis
        """
        self.__x_generator = np.random.default_rng(x_seed)
        self.__y_generator = np.random.default_rng(y_seed)

    def sample_from(self, x_distribution="normal",
                    y_distribution="normal",
                    params=None):
        """
        Sampling function
        :param x_distribution: type of distribution along x-axis
        :param y_distribution: type of distribution along y-axis
        :param params: params of distributions. Dict, where params["x"] is a list of params for x-axis, similarly for y
        :return: (x, y)
        """
        if params is None:
            params = {"x": [0, 1], "y": [0, 1]}
        x, y = 0, 0
        if x_distribution == "normal":
            x = self.__x_generator.normal(*params["x"])
        elif x_distribution == "exponential":
            x = self.__x_generator.exponential(*params["x"])
        if y_distribution == "normal":
            y = self.__y_generator.normal(*params["y"])
        elif y_distribution == "exponential":
            y = self.__y_generator.exponential(*params["y"])
        return x, y
