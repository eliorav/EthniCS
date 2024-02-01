import pandas as pd
from pathlib import Path
from tqdm.auth import tqdm
import pickle
from ..compressed_sensing_tools.services import get_solvers_results, get_sensing_vector
from ..compressed_sensing_tools.sensing_matrix import generate_bernoulli_matrix

def solve_simulations(config, output_folder, exp_path):
    exp_path = Path(exp_path)
    x = pd.read_csv(exp_path).values
    n = x.shape[0]

    for m in tqdm(config.number_of_pools_range):
        phi = generate_bernoulli_matrix(n, m)
        y = get_sensing_vector(phi, x)

        solvers_data = {}
        for i in tqdm(range(y.shape[1])):
            solvers_data[i] = get_solvers_results(phi, y[:,i], config.selected_transformers, config.selected_solvers, should_search_params=True)
        
        with open(output_folder / f"{config.solvers_results_name}_{str(m)}.pkl", "wb") as f_out:
            pickle.dump((x, y, phi, solvers_data), f_out)
