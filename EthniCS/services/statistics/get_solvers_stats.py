import pandas as pd
from tqdm.auto import tqdm
from ...compressed_sensing_tools.metrics import *
from ...compressed_sensing_tools.services import get_sparseness, get_sensing_vector
from .utilities import load_solvers_exp, load_ethnics_exp, get_solvers_stats_file_path
from ...configs.base_config import solvers_results_name, x_ethnics_filename
from ...configs.generate_simulation_config import number_of_pools_range


def get_df_stats(x, y, solvers_data, num_of_pools):
    sol_stats = []
    for ethnicity_num, solvers in solvers_data.items():
        for sol_name, sol_data in solvers.items():
            xhat, ahat, yhat = sol_data
            sol_stats.append(
                {
                    "name": f"{sol_name[1].split(' ')[0]} - {sol_name[0]}"
                    if sol_name != "EthniCS"
                    else sol_name,
                    "num_of_pools": num_of_pools,
                    "ethnicity_num": ethnicity_num,
                    "accuracy_0.05": AccuracyMetric(atol=0.05)(
                        x=x[:, ethnicity_num], xhat=xhat
                    ),
                    "accuracy_0.01": AccuracyMetric(atol=0.01)(
                        x=x[:, ethnicity_num], xhat=xhat
                    ),
                    "psnr": PSNRMetric()(x=x[:, ethnicity_num], xhat=xhat),
                    "psnr_y": PSNRMetric()(x=y[:, ethnicity_num], xhat=yhat),
                    "mse": MSEMetric()(x=x[:, ethnicity_num], xhat=xhat),
                    "x_sparseness": get_sparseness(x[:, ethnicity_num]),
                    "a_sparseness": get_sparseness(ahat),
                    "xhat_sparseness": get_sparseness(xhat),
                }
            )
    return pd.DataFrame(sol_stats)


def get_solvers_stats(experiments_folder):
    df_stats = pd.DataFrame()
    for m in tqdm(number_of_pools_range):
        for exp in experiments_folder.glob(f"**/{x_ethnics_filename}_{m}*"):
            solvers_data_path = list(
                exp.parent.glob(f"**/{solvers_results_name}_{m}*")
            )[0]
            x, y, phi, solvers_data = load_solvers_exp(solvers_data_path)
            xhat_ethnics = load_ethnics_exp(exp)
            yhat_ethnics = get_sensing_vector(phi, xhat_ethnics)

            for ethnicity_num in solvers_data.keys():
                solvers_data[ethnicity_num]["EthniCS"] = (
                    xhat_ethnics[:, ethnicity_num],
                    xhat_ethnics[:, ethnicity_num],
                    yhat_ethnics[:, ethnicity_num],
                )

            df_stats = pd.concat(
                [df_stats, get_df_stats(x, y, solvers_data, num_of_pools=m)],
                ignore_index=True,
            )
    df_stats.to_csv(get_solvers_stats_file_path(experiments_folder), index=False)
