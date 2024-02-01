from .cosamp import cosamp
from ..cs_solver import CsSolver


class CoSaMPSolver(CsSolver):
    """
    CoSaMP solver
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __init__(self, s=10, epsilon=1e-5, max_iter=100):
        s = int(s)
        max_iter = int(max_iter)
        self.s, self.epsilon, self.max_iter = s, epsilon, max_iter

    def __call__(self, phi, y):
        return cosamp(phi, y, self.s, self.epsilon, self.max_iter)

    def get_name(self):
        return f"{self.get_short_name()}: s={self.s}, epsilon={self.epsilon}, max_iter={self.max_iter}"

    def get_short_name(self):
        return "CoSaMP"
