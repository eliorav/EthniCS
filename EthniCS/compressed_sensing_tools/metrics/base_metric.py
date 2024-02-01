from abc import ABC


def select_y(a, ahat, x, xhat, y, yhat):
    """
    Select the y and yhat to the metric
    """
    return (y, yhat)


def select_a(a, ahat, x, xhat, y, yhat):
    """
    Select the "a" and ahat to the metric
    """
    return (a, ahat)


class Metric(ABC):
    """
    A base class for metric object
    """

    def __init__(self, extend_title="", select_params=None):
        """
        param extend_title: extending the title of the metric
        param select_params: a callback function that defines how to select the params for the metric
        """
        self.extend_title, self.select_params = extend_title, select_params

    def __call__(self, a=None, ahat=None, x=None, xhat=None, y=None, yhat=None):
        """
        Calculates the metric
        """

    def get_name(self):
        """
        Returns the name of the metric
        """

    def get_title(self):
        """
        Returns the title of the metric, including the extend title arg
        """
        return f"{self.get_name()} {self.extend_title}"

    def get_units(self):
        """
        Returns the unit of the metric
        """

    def get_params(self, a, ahat, x, xhat, y, yhat):
        """
        A defualt implementation of the select param callback
        """
        return (
            self.select_params(a, ahat, x, xhat, y, yhat)
            if self.select_params is not None
            else (x, xhat)
        )

    def high_is_better(self):
        """
        Returns ture if higer score value is better
        """
        return True
