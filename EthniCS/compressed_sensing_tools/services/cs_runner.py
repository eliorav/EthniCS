from abc import ABCMeta
from .solve_cs import solve_cs
from .optimize_solver_params import optimize_solver_params
from ..constants import param_search_mapping


class CSRunner:
    """
    A pickable class to solve CS problem for a list of solvers and transformations
    """

    def __init__(self, phi, y, should_optimize_params):
        self.phi, self.y, self.should_optimize_params = phi, y, should_optimize_params

    def __call__(self, params):
        Solver, transformer = params
        if self.should_optimize_params and type(Solver) == ABCMeta:
            params = optimize_solver_params(
                Solver,
                self.phi,
                self.y,
                transformer,
                param_search_mapping[Solver().get_short_name()],
            )
            solver = Solver(**params)
        else:
            solver = Solver()

        print(transformer.get_name(), solver.get_short_name())
        return (
            (transformer.get_name(), solver.get_short_name()),
            solve_cs(self.phi, self.y, solver, transformer),
        )
