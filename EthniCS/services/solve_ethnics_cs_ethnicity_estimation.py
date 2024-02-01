import numpy as np
from ..compressed_sensing_tools.services import get_ethnics_solution

def solve_ethnics_cs_ethnicity_estimation(phi, y, solvers_data, similar_solvers=[], threshold=0.9):
    """
    Get the EthniCS solution for ethnicity estimation using CS
    """
    x_res = np.zeros((phi.shape[1], y.shape[1]))
    probabilities = []

    for ethnicity_num in range(y.shape[1]):
        x_res[:, ethnicity_num], probability = get_ethnics_solution(
            phi,
            y[:, ethnicity_num],
            solvers_data[ethnicity_num],
            similar_solvers=similar_solvers,
            threshold=threshold,
        )
        probabilities += [probability]
    return x_res, probabilities
