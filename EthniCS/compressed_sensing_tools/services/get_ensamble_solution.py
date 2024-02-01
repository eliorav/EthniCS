import numpy as np
from skimage.metrics import peak_signal_noise_ratio
from .get_sparseness import get_sparseness
from .fine_tune_result import fine_tuning_result


def get_ensamble_solution(phi, y, solvers_data, threshold=0.9):
    """
    Returns the best solution from a list of solvers results for the CS problem
    """
    dence_scores = []
    sparseness = []
    sparse_scores = []

    solvers_data_values = list(solvers_data.values())
    for sol_data in solvers_data_values:
        _, a_hat, y_hat = sol_data
        signal_sparseness = get_sparseness(a_hat)
        sparseness.append(signal_sparseness)
        psnr_score = peak_signal_noise_ratio(y, y_hat, data_range=1)

        # The score is the sparseness of the signal and the fittest to y (using PSNR score)
        score = signal_sparseness + 5 * psnr_score
        dence_score = -signal_sparseness

        sparse_scores.append(score)
        dence_scores.append(dence_score)

    # If we found a sparse solution, we can assume that the signal is sparse
    max_sparseness = np.array(sparseness).max()
    is_sparse = max_sparseness > int(phi.shape[1] * threshold)

    # If the signal is sparse - get the result with the best score
    # if the signal is not sparse - get the most dence result
    best_idx = (
        np.array(sparse_scores).argmax()
        if is_sparse
        else np.array(dence_scores).argmax()
    )
    x_res = solvers_data_values[best_idx][0]

    return fine_tuning_result(phi, x_res, y, max_iter=5000) if is_sparse else x_res
