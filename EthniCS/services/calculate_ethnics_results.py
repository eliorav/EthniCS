import pickle
from tqdm import tqdm
from .solve_ethnics import solve_ethnics
from ..configs.base_config import BaseConfig
from ..compressed_sensing_tools.EthniCS import EthniCS
from ..compressed_sensing_tools.EthniCS_config import EthniCSConfig


def calculate_ethnics_results(config:BaseConfig, ethnics_config:EthniCSConfig, output_folder):
    """
    Calculate EthniCS results for the experiments.

    Args:
        config (Config): The configuration object.
        output_folder (str): The path to the output folder.
    """
    ethnics_calculator = EthniCS(ethnics_config)
    similar_solvers = config.similar_solvers or []

    for f in tqdm(output_folder.glob(f"**/{config.solvers_results_name}_*.pkl")):
        m = int(f.name.split("_")[-1].split(".")[0])

        with open(f, "rb") as f_in:
            x, y, phi, solvers_data = pickle.load(f_in)
            x_res, confidences = solve_ethnics(phi, y, solvers_data, similar_solvers, ethnics_calculator)
            
            with open(f.parent / f"{config.x_ethnics_filename}_{str(m)}.pkl", "wb") as f_out:
                pickle.dump((x_res, confidences), f_out)
