import numpy as np
from .gpsr import gpsr_bb
from ..cs_solver import CsSolver


class GPSRBBSolver(CsSolver):
    """
    GPSR-BB solver
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __init__(
        self,
        tau=1e-2,
        initial_solution=None,
        alpha0=1,
        alpha_lims=None,
        tolerance=1e-1,
        iter_max=10000,
    ):
        (
            self.initial_solution,
            self.tau,
            self.alpha0,
            self.alpha_lims,
            self.tolerance,
            self.iter_max,
        ) = (initial_solution, tau, alpha0, alpha_lims, tolerance, int(iter_max))

    def __call__(self, phi, y):
        initial_solution = (
            self.initial_solution
            if self.initial_solution is not None
            else np.zeros(phi.shape[1])
        )
        return gpsr_bb(
            initial_solution,
            phi,
            y,
            self.tau,
            self.alpha0,
            self.alpha_lims,
            self.tolerance,
            self.iter_max,
        )

    def get_name(self):
        return f"{self.get_short_name()} - tau-{self.tau}, alpha0={self.alpha0}, alpha_lims={self.alpha_lims}, tolerance={self.tolerance}, iter_max={self.iter_max}"

    def get_short_name(self):
        return "GPSR-BB"
