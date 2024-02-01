import numpy as np
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.linear_model import OrthogonalMatchingPursuitCV
from .cs_solver import CsSolver


class OMPSolver(CsSolver):
    """
    OMP solver
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __init__(self, n_nonzero_coefs=10):
        self.n_nonzero_coefs = int(n_nonzero_coefs)

    def __call__(self, phi, y):
        omp = OrthogonalMatchingPursuit(n_nonzero_coefs=self.n_nonzero_coefs)
        omp.fit(phi, y)
        x_hat = omp.coef_
        return np.reshape(x_hat, [-1])

    def get_name(self):
        return f"{self.get_short_name()} - n_nonzero_coefs={self.n_nonzero_coefs}"

    def get_short_name(self):
        return "OMP"


class OMPCVSolver(CsSolver):
    """
    OMP-CV solver
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __call__(self, phi, y):
        omp_cv = OrthogonalMatchingPursuitCV()
        omp_cv.fit(phi, y)
        x_hat = omp_cv.coef_
        return np.reshape(x_hat, [-1])

    def get_name(self):
        return f"{self.get_short_name()}"

    def get_short_name(self):
        return "OMP-CV"

