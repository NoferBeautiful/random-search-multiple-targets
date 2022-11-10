import numpy as np


def gaussian_mixture(x, mu, sigma, mu0, sigma0):
    first = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma * sigma))
    second = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x + mu) ** 2 / (2 * sigma * sigma))
    center = 1 / (sigma0 * np.sqrt(2 * np.pi)) * np.exp(-(x - mu0) ** 2 / (2 * sigma0 * sigma0))
    return 1 / 7 * first + 5 / 7 * center + 1 / 7 * second


def exponential_mixture(x, lambda_):
    result = np.zeros(x.shape)
    result[x >= 0] = 1 / 2 * lambda_ * np.exp(-lambda_ * x[x >= 0])
    result[x < 0] = 1 / 2 * lambda_ * np.exp(lambda_ * x[x < 0])
    return result


def get_params_for_distribution(distr_type, variance):
    modifier = 10
    if distr_type == 'gaussian_mixture':
        params = [10, 1, 0, 2]
        params[0] += variance / modifier
        params[3] += 0.5 * variance / modifier
        return params
    elif distr_type == 'exponential_mixture':
        params = 1 / (variance / modifier + 1)
        return params
    else:
        raise NotImplemented


def distribution_plot(x, distr_type, variance):
    params = get_params_for_distribution(distr_type, variance)
    if distr_type == 'gaussian_mixture':
        return gaussian_mixture(x, *params)
    elif distr_type == 'exponential_mixture':
        return exponential_mixture(x, params)
    else:
        raise NotImplemented


def sample_from_gaussian_mixture(generator, params):
    mixture = generator.uniform(0, 1)
    if mixture < 1 / 7:
        return generator.normal(-params[0], params[1])
    elif mixture > 6 / 7:
        return generator.normal(params[0], params[1])
    return generator.normal(params[2], params[3])


def sample_from_exponential_mixture(generatorm, param):
    sign = 2 * generatorm.binomial(1, 0.5) - 1
    return generatorm.exponential(sign * param)


class DotSampler:
    def __init__(self, x_seed=None, y_seed=None):
        """
        DotSampler initialization
        :param x_seed: random generator seed for x-axis
        :param y_seed: random generator seed for y-axis
        """
        self.__x_generator = np.random.default_rng(x_seed)
        self.__y_generator = np.random.default_rng(y_seed)

    def sample_from(self, x_distribution="gaussian_mixture",
                    y_distribution="gaussian_mixture",
                    variance=0):
        """
        Sampling function
        :param x_distribution: type of distribution along x-axis
        :param y_distribution: type of distribution along y-axis
        :param variance: variance to find mixture params
        :return: (x, y)
        """
        x, y = 0, 0
        if x_distribution == "gaussian_mixture":
            params = get_params_for_distribution(x_distribution, variance)
            x = sample_from_gaussian_mixture(self.__x_generator, params)
        elif x_distribution == "exponential_mixture":
            params = get_params_for_distribution(x_distribution, variance)
            x = sample_from_exponential_mixture(self.__x_generator, params)
        if y_distribution == "gaussian_mixture":
            params = get_params_for_distribution(y_distribution, variance)
            y = sample_from_gaussian_mixture(self.__y_generator, params)
        elif y_distribution == "exponential_mixture":
            params = get_params_for_distribution(y_distribution, variance)
            y = sample_from_exponential_mixture(self.__y_generator, params)
        return np.array([x, y])
