from tqdm import tqdm
import pandas as pd
import pickle
from ..compressed_sensing_tools.services import get_solvers_results, get_sensing_vector
from ..compressed_sensing_tools.sensing_matrix import generate_bernoulli_matrix
from ..configs.base_config import BaseConfig

def generate_real_data_experiments(ethnicities_df, config: BaseConfig, output_folder):
    """
    Generate real data experiments.

    This function generates real data experiments by sampling random individuals from a given ethnicity file,
    creating sensing vectors using a Bernoulli matrix, and obtaining solver results for each sensing vector.

    Args:
        ethnicities_df (pandas.DataFrame): The DataFrame containing the ethnicity data.
        config (BaseConfig): The configuration object containing various settings.
        output_folder (str): The output folder path to save the experiment results.
    """
    
    n = config.number_of_individuals

    for exp_idx in range(1, config.num_of_exp+1):
        x = ethnicities_df.sample(n=n).values # Sample random n individuals for the experiment 

        exp_name = f"exp_{exp_idx}"
        exp_folder = output_folder/exp_name
        exp_folder.mkdir(exist_ok=True, parents=True)
        
        for m in tqdm(config.number_of_pools_range):
            phi = generate_bernoulli_matrix(n, m)
            y = get_sensing_vector(phi, x)

            solvers_data = {}
            for i in tqdm(range(y.shape[1])):
                solvers_data[i] = get_solvers_results(phi, y[:,i], config.selected_transformers, config.selected_solvers, should_search_params=config.should_search_params)

            with open(exp_folder / f"{config.solvers_results_name}_{str(m)}.pkl", "wb") as f_out:
                pickle.dump((x, y, phi, solvers_data), f_out)