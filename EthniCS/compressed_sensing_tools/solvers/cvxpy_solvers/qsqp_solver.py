import numpy as np
import cvxpy as cvx
from .cvxpy_solver import CvxpySolver


class OSQPSolver(CvxpySolver):
    """
    OSQP solver
    """

    __doc__ = CvxpySolver.__doc__ + __doc__

    def __init__(self, verbose=False, max_iter=10000, eps_abs=1e-5, eps_rel=1e-5):
        self.solver = "OSQP"
        self.verbose = verbose
        self.params = {
            "max_iter": int(max_iter),
            "eps_abs": eps_abs,
            "eps_rel": eps_rel,
        }

    def __call__(self, phi, y):
        vx = cvx.Variable(phi.shape[1])
        objective = cvx.Minimize(cvx.norm(vx, 1))
        constraints = [phi @ vx == y]
        prob = cvx.Problem(objective, constraints)
        result = prob.solve(solver=self.solver, verbose=self.verbose, **self.params)
        return np.array(vx.value).squeeze()

    def get_name(self):
        return self.get_short_name()

    def get_short_name(self):
        return "OSQP"
