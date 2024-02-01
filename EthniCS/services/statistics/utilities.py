import pickle
from .constants import solvers_stats_filename


def get_solver_short_name(sol_name):
    """
    Returns a short name for the solver and transformer

    Parameters:
    sol_name (str): The name of the solver and transformer
    """
    return f"{sol_name[1].split(' ')[0]} - {sol_name[0]}"


def load_solvers_exp(exp):
    """
    Open the solvers experiment results

    Parameters:
    exp (str): The path to the experiment results file

    Returns:
    tuple: A tuple containing the experiment data (x, y, phi, solvers_data)
    """
    with open(exp, "rb") as f_in:
        x, y, phi, solvers_data = pickle.load(f_in)
    return x, y, phi, solvers_data


def load_ethnics_exp(exp):
    """
    Open the ethnics experiment results

    Parameters:
    exp (str): The path to the experiment results file

    Returns:
    object: The loaded experiment data
    """
    with open(exp, "rb") as f_in:
        xhat = pickle.load(f_in)
    return xhat


def get_stats_folder(experiments_folder):
    """
    Get the folder path for storing statistics

    Parameters:
    experiments_folder (str): The path to the experiments folder

    Returns:
    str: The path to the statistics folder
    """
    return experiments_folder / "stats"


def get_solvers_stats_file_path(experiments_folder):
    """
    Get the file path for storing solvers statistics

    Parameters:
    experiments_folder (str): The path to the experiments folder

    Returns:
    str: The path to the solvers statistics file
    """
    return get_stats_folder(experiments_folder) / solvers_stats_filename,
