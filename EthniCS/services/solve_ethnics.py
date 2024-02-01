import numpy as np
from ..compressed_sensing_tools.services import get_ethnics_solution

def solve_ethnics(phi, y, solvers_data, similar_solvers=[], threshold=0.9):
    """
    Get the EthniCS solution for a given sensing matrix, measurement vector and solvers results.

    Parameters:
    phi (numpy.ndarray): Sensing matrix of shape (m, n).
    y (numpy.ndarray): Measurement vector of shape (m, k).
    solvers_data (list): List of solver data for each ethnicity.
    similar_solvers (list, optional): List of similar solvers to consider. Defaults to [].
    threshold (float, optional): Threshold value for solver selection. Defaults to 0.9.

    Returns:
    tuple: A tuple containing the estimated solution matrix x_res of shape (n, k) and a list of probabilities for each ethnicity.
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
