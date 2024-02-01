import numpy as np
from .base_metric import Metric


def calc_accuracy(a, b, atol):
    """
    Return and accuracy between a and b using tolerance
    """
    assert len(a) == len(b)
    np_a = np.asarray(a)
    return np.isclose(a, b, atol=atol).astype(int).sum() / (np_a.size)


class AccuracyMetric(Metric):
    """
    Accuracy metric
    """

    __doc__ = Metric.__doc__ + __doc__

    def __init__(self, atol, extend_title="", select_params=None):
        extend_title = f"{extend_title}- tol={atol}" 
        super(AccuracyMetric, self).__init__(extend_title, select_params)
        self.atol = atol

    def __call__(self, a=None, ahat=None, x=None, xhat=None, y=None, yhat=None):
        param1, param2 = self.get_params(a, ahat, x, xhat, y, yhat)
        return calc_accuracy(param1, param2, atol=self.atol)

    def get_name(self):
        return "Accuracy"

    def get_units(self):
        return "accuracy"
