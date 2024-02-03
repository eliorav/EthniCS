import numpy as np
from ..compressed_sensing_tools.EthniCS import EthniCS

def solve_ethnics(phi, y, solvers_data, similar_solvers, ethnics_calculator:EthniCS):
    """
    Get the EthniCS solution for a given sensing matrix, measurement vector and solvers results.

    Parameters:
    phi (numpy.ndarray): Sensing matrix of shape (m, n).
    y (numpy.ndarray): Measurement vector of shape (m, k).
    solvers_data (list): List of solver data for each ethnicity.
    similar_solvers (list, optional): List of similar solvers to consider. Defaults to [].
    ethnics_calculator (EthniCS): Instance of the EthniCS class.

    Returns:
    tuple: A tuple containing the estimated solution matrix x_res of shape (n, k) and a list of probabilities for each ethnicity.
    """
    x_res = np.zeros((phi.shape[1], y.shape[1]))
    confidences = []

    for ethnicity_num in range(y.shape[1]):
        x_res[:, ethnicity_num], confidence = ethnics_calculator.solve(
            phi,
            y[:, ethnicity_num],
            solvers_data[ethnicity_num],
            similar_solvers=similar_solvers,
        )
        confidences += [confidence]
    return x_res, confidences
