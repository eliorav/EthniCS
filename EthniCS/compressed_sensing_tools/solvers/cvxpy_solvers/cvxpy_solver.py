import cvxpy as cvx
import numpy as np
from ..cs_solver import CsSolver


class CvxpySolver(CsSolver):
    """
    A base class for CVXPY solvers
    """

    __doc__ = CsSolver.__doc__ + __doc__

    def __init__(self, solver, verbose=False, **kwargs):
        self.solver, self.verbose, self.kwargs = solver, verbose, kwargs

    def __call__(self, phi, y):
        vx = cvx.Variable(phi.shape[1])
        objective = cvx.Minimize(cvx.norm(vx, 1))
        constraints = [phi @ vx == y]
        prob = cvx.Problem(objective, constraints)
        result = prob.solve(solver=self.solver, verbose=self.verbose, **self.kwargs)
        return np.array(vx.value).squeeze()

    def get_name(self):
        return self.get_short_name()

    def get_short_name(self):
        return f"CVXPY - solver={self.solver}"
