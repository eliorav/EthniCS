import pandas as pd
import numpy as np
from pathlib import Path
from tqdm.auto import tqdm

from ...compressed_sensing_tools import EthniCS
from ...compressed_sensing_tools.EthniCS_config import EthniCSConfig
from ...compressed_sensing_tools.metrics import *
from ...compressed_sensing_tools.services import get_sparseness, get_sensing_vector
from .utilities import load_solvers_exp, load_ethnics_exp, get_solvers_stats_file_path
from ...configs.base_config import BaseConfig
from .constants import base_line_solver
from ...constants import ETHNICS_SOLVER

def get_stats_obj(name, num_of_pools, ethnicity_num, x, y, xhat, yhat, ahat, exp_num, confidence=0):
    x_clean = np.copy(x)
    x_clean[x_clean < 0.1] = 0

    return {
        "name": name,
        "exp_num": exp_num,
        "num_of_pools": num_of_pools,
        "ethnicity_num": ethnicity_num,
        "accuracy_0.05": AccuracyMetric(atol=0.05)(x=x, xhat=xhat),
        "accuracy_0.01": AccuracyMetric(atol=0.01)(x=x, xhat=xhat),
        "psnr": PSNRMetric()(x=x, xhat=xhat),
        "psnr_y": PSNRMetric()(x=y, xhat=yhat),
        "mse": MSEMetric()(x=x, xhat=xhat),
        "x_sparseness": get_sparseness(x),
        "a_sparseness": get_sparseness(ahat),
        "xhat_sparseness": get_sparseness(xhat),
        "confidence": confidence,
        "original_sparsity_ratio": round(np.count_nonzero(x_clean)/len(x_clean), 2),
    }

def get_base_line_stats_obj(n, m, x, y, num_of_pools, ethnicity_num, exp_num):
    x_base_line = np.zeros(n)
    a_base_line = np.zeros(n)
    y_base_line = np.zeros(m)

    return get_stats_obj(
        name=base_line_solver,
        num_of_pools=num_of_pools,
        ethnicity_num=ethnicity_num,
        x=x,
        y=y,
        xhat=x_base_line,
        yhat=y_base_line,
        ahat=a_base_line,
        exp_num=exp_num,
    )

def get_df_stats(x, y, solvers_data, confidences, num_of_pools, exp_num):
    """
    Calculate statistics for each solver and EthniCS.

    Args:
        x (numpy.ndarray): The original signal matrix.
        y (numpy.ndarray): The sensed signal matrix.
        solvers_data (dict): A dictionary containing solver data for each ethnicity.
        num_of_pools (int): The number of pools used in the experiment.

    Returns:
        pandas.DataFrame: A DataFrame containing the statistics for each solver and EthniCS.
    """
    
    sol_stats = []
    for ethnicity_num, solvers in solvers_data.items():
        confidence = confidences[ethnicity_num]

        for sol_name, sol_data in solvers.items():
            xhat, ahat, yhat = sol_data
            name = f"{sol_name[1].split(' ')[0]} - {sol_name[0]}" if sol_name != ETHNICS_SOLVER else sol_name

            sol_stats.append(get_stats_obj(
                name=name,
                num_of_pools=num_of_pools,
                ethnicity_num=ethnicity_num,
                x=x[:, ethnicity_num],
                y=y[:, ethnicity_num],
                xhat=xhat,
                yhat=yhat,
                ahat=ahat,
                confidence=confidence if sol_name == ETHNICS_SOLVER else 0,
                exp_num=exp_num,
            ))

        sol_stats.append(get_base_line_stats_obj(
            n=x.shape[0], 
            m=y.shape[0], 
            x=x[:, ethnicity_num],
            y=y[:, ethnicity_num],
            num_of_pools=num_of_pools, 
            ethnicity_num=ethnicity_num,
            exp_num=exp_num,
        ))
        
    return pd.DataFrame(sol_stats)


def calculate_solvers_stats(experiments_folder, config: BaseConfig, ethnics_config_path: str='./EthniCS_config.json', recalculate_confidences=False):
    """
    Calculate statistics for solvers using different experiment configurations.

    Args:
        experiments_folder (str): The path to the folder containing the experiment data.
    """
    ethnics_config = EthniCSConfig.from_json(ethnics_config_path)
    ethnics_solver = EthniCS(ethnics_config)
    
    df_stats = pd.DataFrame()
    for m in tqdm(config.number_of_pools_range):
        for exp in experiments_folder.glob(f"**/{config.x_ethnics_filename}_{m}*"):
            solvers_data_path = list(
                exp.parent.glob(f"**/{config.solvers_results_name}_{m}*")
            )[0]
            x, y, phi, solvers_data = load_solvers_exp(solvers_data_path)
            xhat_ethnics, confidences = load_ethnics_exp(exp)
            yhat_ethnics = get_sensing_vector(phi, xhat_ethnics)

            if recalculate_confidences:
                confidences = [ethnics_solver.get_best_solver(phi, y[:,i], solvers_data[i], similar_solvers=config.similar_solvers)[1] for i in range(y.shape[1])]

            for ethnicity_num in solvers_data.keys():
                solvers_data[ethnicity_num][ETHNICS_SOLVER] = (
                    xhat_ethnics[:, ethnicity_num],
                    xhat_ethnics[:, ethnicity_num],
                    yhat_ethnics[:, ethnicity_num],
                )

            df_stats = pd.concat(
                [df_stats, get_df_stats(x, y, solvers_data, confidences, exp_num=exp.parent.name, num_of_pools=m)],
                ignore_index=True,
            )

    output_file = Path(get_solvers_stats_file_path(experiments_folder))
    output_file.parent.mkdir(exist_ok=True, parents=True)
    df_stats.to_csv(output_file, index=False)
