import pylops
from ..cs_solver import CsSolver


def get_kind(value):
    """
    Retruns the king of thresholding
    """
    kinds = {
        0: "hard",
        1: "soft",
        2: "half",
        3: "hard-percentile",
        4: "soft-percentile",
        5: "half-percentile",
    }
    return kinds[value]


class ISTASolver(CsSolver):
    """
    ISTA solver
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __init__(self, **kwargs):
        kwargs["niter"] = int(kwargs.get("niter", 0))
        kwargs["threshkind"] = get_kind(round(kwargs.get("threshkind", 0)))
        self.kwargs = kwargs

    def __call__(self, phi, y):
        res = pylops.optimization.sparsity.ISTA(
            pylops.MatrixMult(phi), y, **self.kwargs
        )

        return res[0]

    def get_name(self):
        return f"{self.get_short_name()} - {self.kwargs}"

    def get_short_name(self):
        return "ISTA"

