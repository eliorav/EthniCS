import numpy as np
import cvxpy as cvx
from .cvxpy_solver import CvxpySolver


class SCSSolver(CvxpySolver):
    """
    SCS solver
    """

    __doc__ = CvxpySolver.__doc__ + __doc__

    def __init__(
        self,
        verbose=False,
        max_iters=2500,
        eps=1e-4,
        alpha=1.8,
        scale=5.0,
        normalize=True,
        use_indirect=True,
    ):
        self.solver = "SCS"
        self.verbose = verbose
        self.scs_params = {
            "max_iters": int(max_iters),
            "eps": eps,
            "alpha": alpha,
            "scale": scale,
        }

    def __call__(self, phi, y):
        vx = cvx.Variable(phi.shape[1])
        objective = cvx.Minimize(cvx.norm(vx, 1))
        constraints = [phi @ vx == y]
        prob = cvx.Problem(objective, constraints)
        result = prob.solve(solver=self.solver, verbose=self.verbose, **self.scs_params)
        return np.array(vx.value).squeeze()

    def get_name(self):
        return self.get_short_name()

    def get_short_name(self):
        return "SCS"

