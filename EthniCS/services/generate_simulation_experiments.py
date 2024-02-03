import numpy as np
import pandas as pd
from tqdm.auto import tqdm
import pickle
from ..compressed_sensing_tools.services import get_solvers_results, get_sensing_vector
from ..compressed_sensing_tools.sensing_matrix import generate_bernoulli_matrix
from ..configs.generate_simulation_config import SimulationDataConfig

def generate_random_vector(n, sparsity_ratio):
    """
    Generate a random vector with a given sparsity ratio.

    Args:
        n (int): Length of the vector.
        sparsity_ratio (float): Sparsity ratio of the vector.

    Returns:
        numpy.ndarray: Random vector with the specified sparsity ratio.
    """
    X = np.zeros(n)
    selected_idx = np.random.choice(range(n), round(sparsity_ratio * n))
    X[selected_idx] = np.random.rand(len(selected_idx))

    return X

def generate_single_exp(n, sparsity_ratios):
    """
    Generate a single experiment with multiple sparse ratios.

    Args:
        n (int): Length of the vectors.
        sparsity_ratios (numpy.ndarray, optional): Array of sparse ratios.

    Returns:
        numpy.ndarray: Array of generated vectors with different sparse ratios.
    """
    return pd.DataFrame({str(int(sparsity_ratio*100)): generate_random_vector(n, sparsity_ratio)  for sparsity_ratio in sparsity_ratios}).values

def generate_simulation_experiments(config: SimulationDataConfig, output_folder):
    """
    Generate experiments for EthniCS.
    The code create random simulation data, generate sensing matrix and measurement vector and run the solvers on the data.

    Args:
        config (SimulationDataConfig): Configuration object containing parameters for the simulations.
        output_folder (str): Path to the output folder where the results will be saved.
    """
    n = config.number_of_individuals
    x = generate_single_exp(n, config.sparsity_ratios)

    for m in tqdm(config.number_of_pools_range):
        phi = generate_bernoulli_matrix(n, m)
        y = get_sensing_vector(phi, x)

        solvers_data = {}
        for i in tqdm(range(y.shape[1])):
            solvers_data[i] = get_solvers_results(phi, y[:,i], config.selected_transformers, config.selected_solvers, should_search_params=True)
        
        with open(output_folder / f"{config.solvers_results_name}_{str(m)}.pkl", "wb") as f_out:
            pickle.dump((x, y, phi, solvers_data), f_out)
