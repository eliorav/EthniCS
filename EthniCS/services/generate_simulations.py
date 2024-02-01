import argparse
from pathlib import Path
from tqdm.auto import tqdm
import pickle
from ..compressed_sensing_tools.services import get_solvers_results, get_sensing_vector
from ..compressed_sensing_tools.sensing_matrix import generate_bernoulli_matrix
from .generate_ethnicity_matrix import generate_ethnicity_matrix

def load_ethnicity_distribution(ethnicity_distribution_path):
    with open(ethnicity_distribution_path, "rb") as f_in:
        return pickle.load(f_in)

def generate_simulations(args, config, output_folder):
    ethnicity_distribution = load_ethnicity_distribution(args.ethnicity_distribution_path)
    n = args.number_of_individuals

    for exp in range(1, args.num_of_exp+1):
        x = generate_ethnicity_matrix(ethnicity_distribution, n=n)

        exp_name = f"exp{exp}" if args.exp_name is None else f"exp_{args.exp_name}{'' if args.num_of_exp == 1 else exp}"
        exp_folder = output_folder/exp_name
        exp_folder.mkdir(exist_ok=True, parents=True)
        for m in tqdm(config.number_of_pools_range):
            phi = generate_bernoulli_matrix(n, m)
            y = get_sensing_vector(phi, x)

            solvers_data = {}
            for i in tqdm(range(y.shape[1])):
                solvers_data[i] = get_solvers_results(phi, y[:,i], config.selected_transformers, config.selected_solvers, should_search_params=True)
            
            with open(exp_folder / f"{config.solvers_results_name}_{str(m)}.pkl", "wb") as f_out:
                pickle.dump((x, y, phi, solvers_data), f_out)
