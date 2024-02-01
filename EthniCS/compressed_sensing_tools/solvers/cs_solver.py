from abc import ABC


class CsSolver(ABC):
    """
    A CS solver
    """

    def __call__(self, phi, y):
        """
        Solve the CS problem
        param phi: the sensing matrix
        param y: the measurement vector
        """

    def get_name(self):
        """
        Returns the full name of the solver, including params
        """

    def get_short_name(self):
        """
        Returns the short name of the solver
        """

