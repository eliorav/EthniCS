import pylops
from .ista_solver import ISTASolver


class FISTASolver(ISTASolver):
    """
    FISTA solver
    """

    __doc__ = ISTASolver.__doc__ + __doc__

    def __call__(self, phi, y):
        res = pylops.optimization.sparsity.FISTA(
            pylops.MatrixMult(phi), y, **self.kwargs
        )

        return res[0]

    def get_short_name(self):
        return "FISTA"
