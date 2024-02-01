import numpy as np
from .base_metric import Metric


def mse(a1, a2):
    """
    Returns MSE between a1 and a2
    """
    return np.mean((a1 - a2) ** 2)


class MSEMetric(Metric):
    """
    MSE metric
    """

    __doc__ = Metric.__doc__ + __doc__

    def __call__(self, a=None, ahat=None, x=None, xhat=None, y=None, yhat=None):
        param1, param2 = self.get_params(a, ahat, x, xhat, y, yhat)
        return mse(param1, param2)

    def get_name(self):
        return "MSE"

    def get_units(self):
        return "error"

    def high_is_better(self):
        return False
