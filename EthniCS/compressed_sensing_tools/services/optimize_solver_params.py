import math
import numpy as np
from bayes_opt import BayesianOptimization
from skimage.metrics import peak_signal_noise_ratio
from .solve_cs import solve_cs

import warnings
warnings.filterwarnings("ignore", category=Warning)


def get_psnr_score(phi, y, xhat, ahat, yhat):
    """
    Returns PSNR score for the optimization process
    """
    return peak_signal_noise_ratio(y, yhat, data_range=1)


def optimize_solver_params(
    Solver, phi, y, transformer, search_params, get_score=get_psnr_score, max_score=1000
):
    """
    Optimize the params of a solver for a given CS problem
    """

    def train(**kwargs):
        score = 0

        solver = Solver(**kwargs)
        try:
            xhat, ahat, yhat = solve_cs(phi, y, solver, transformer)
            score = get_score(phi, y, xhat, ahat, yhat)
            if math.isinf(score):
                score = max_score
        except Exception as e:
            print("ELIOR", e)

        return score

    optimizer = BayesianOptimization(
        train, search_params, random_state=27, verbose=False
    )

    optimizer.maximize()
    print(optimizer.max)
    return optimizer.max["params"]
