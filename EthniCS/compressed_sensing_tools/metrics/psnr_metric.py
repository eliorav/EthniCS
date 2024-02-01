import numpy as np
from skimage.metrics import peak_signal_noise_ratio
from .base_metric import Metric


class PSNRMetric(Metric):
    """
    PSNR metric
    """

    __doc__ = Metric.__doc__ + __doc__

    def __call__(self, a=None, ahat=None, x=None, xhat=None, y=None, yhat=None):
        param1, param2 = self.get_params(a, ahat, x, xhat, y, yhat)
        return peak_signal_noise_ratio(param1, param2, data_range=1)

    def get_name(self):
        return "PSNR"

    def get_units(self):
        return "dB"

