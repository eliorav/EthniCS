import pickle
from .constants import solvers_stats_filename


def get_solver_short_name(sol_name):
    """
    Returns a short name for the solver and transformer
    """
    return f"{sol_name[1].split(' ')[0]} - {sol_name[0]}"


def load_solvers_exp(exp):
    """
    open the solvers experiment results
    """
    with open(exp, "rb") as f_in:
        x, y, phi, solvers_data = pickle.load(f_in)
    return x, y, phi, solvers_data


def load_ethnics_exp(exp):
    """
    open the ethnics experiment results
    """
    with open(exp, "rb") as f_in:
        xhat = pickle.load(f_in)
    return xhat


def get_stats_folder(experiments_folder):
    return experiments_folder / "stats"


def get_solvers_stats_file_path(experiments_folder):
    return get_stats_folder(experiments_folder) / solvers_stats_filename,
