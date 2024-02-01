import numpy as np
from sklearn.linear_model import Lasso
from .cs_solver import CsSolver


class LassoSolver(CsSolver):
    """
    Lasso solver
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __init__(self, alpha=1e-5, max_iter=10000, positive=True):
        self.alpha = alpha
        self.max_iter = int(max_iter)
        self.positive = (positive if type(positive) == bool else positive > 0.5)

    def __call__(self, phi, y):
        lasso_est = Lasso(
            alpha=self.alpha, max_iter=self.max_iter, positive=self.positive
        )
        lasso_est.fit(phi, y)
        x_hat = lasso_est.coef_
        return np.reshape(x_hat, [-1])

    def get_name(self):
        return f"{self.get_short_name()} - alpha={self.alpha}, max_iter={self.max_iter}, positive={self.positive}"

    def get_short_name(self):
        return "LASSO"

