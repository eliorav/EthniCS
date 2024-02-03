from tqdm import tqdm
import pandas as pd
from .generate_real_data_experiments import generate_real_data_experiments
from ..configs.generate_super_population_experiments_config import SuperPopulationConfig

def generate_super_population_experiments(ethnicities_df, config: SuperPopulationConfig, output_folder):
    selected_ethnicity_samples = ethnicities_df[ethnicities_df[config.selected_ethnicity] > config.ethnicity_threshold]
    remaining_samples = ethnicities_df[~ethnicities_df['sample'].isin(selected_ethnicity_samples['sample'])]

    for sparsity_ratio in config.sparsity_ratios:
        exp_folder = output_folder/f"sparsity_{sparsity_ratio}"
        exp_folder.mkdir(exist_ok=True, parents=True)

        ethnicity_indi_selection_count = round(sparsity_ratio * config.number_of_individuals)
        remaining_count = config.number_of_individuals - ethnicity_indi_selection_count
        selected_samples = pd.concat([selected_ethnicity_samples.sample(n=ethnicity_indi_selection_count), remaining_samples.sample(n=remaining_count)]).set_index('sample')

        generate_real_data_experiments(selected_samples, config, exp_folder)