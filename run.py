import pandas as pd
from fire import Fire
from pathlib import Path
from EthniCS.compressed_sensing_tools.EthniCS_config import EthniCSConfig
from EthniCS.configs.get_config_by_type import get_config_by_type, ConfigType
from EthniCS.services.convert_iadmix_output import convert_iadmix_output as convert_iadmix_output_service
from EthniCS.services.calculate_ethnics_results import calculate_ethnics_results as calculate_ethnics_results_service
from EthniCS.services.generate_real_data_experiments import generate_real_data_experiments as generate_real_data_experiments_service
from EthniCS.services.generate_simulation_experiments import generate_simulation_experiments as generate_simulation_experiments_service
from EthniCS.services.generate_super_population_experiments import generate_super_population_experiments as generate_super_population_experiments_service
from EthniCS.services.statistics.calculate_solvers_stats import calculate_solvers_stats

def convert_iadmix_output(iadmix_output_folder:Path='./data/iadmix_output_example', output_folder:Path='./iadmix_output'):
    """
    Convert iAdmix output to a CSV file.

    Args:
        iadmix_output_folder (Path): The folder containing the iAdmix output files. Defaults to './data/iadmix_output_example'.
        output_folder (Path): The output folder to save the converted CSV file. Defaults to './iadmix_output'.
    """
    iadmix_output_folder = Path(iadmix_output_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)

    convert_iadmix_output_service(iadmix_output_folder, output_folder)

def calculate_ethnics_results(config_type:ConfigType, output_folder: Path='./simulations_output', ethnics_config_file:Path='./EthniCS_config.json'):
    """
    Calculate EthniCS results based on the given configuration type.

    Args:
        config_type (ConfigType): The type of configuration to use for calculating EthniCS results.
        output_folder (str, optional): The output folder to save the results. Defaults to './simulations_output'.
        ethnics_config_file (str, optional): The path to the EthniCS configuration file. Defaults to './EthniCS_config.json'.
    """
    output_folder = Path(output_folder).absolute()
    output_folder.mkdir(exist_ok=True, parents=True)

    config = get_config_by_type(config_type)
    ethnics_config = EthniCSConfig.from_json(ethnics_config_file)

    calculate_ethnics_results_service(config, ethnics_config, output_folder)

def generate_simulation_experiments(output_folder:Path='./simulations_output', no_ethnics:bool=False, no_stats:bool=False, ethnics_config_file:Path='./EthniCS_config.json'):
    """
    Generate simulation experiments based on the given configuration type and solve it with EthniCS.

    Args:
        output_folder (str, optional): The output folder to save the simulation experiments. Defaults to './simulations_output'.
        no_ethnics (bool, optional): Flag to indicate whether to skip calculating EthniCS results. Defaults to False.
        no_stats (bool, optional): Flag to indicate whether to skip calculating solver statistics. Defaults to False.
        ethnics_config_file (str, optional): The path to the EthniCS configuration file. Defaults to './EthniCS_config.json'.
    """
    output_folder = Path(output_folder).absolute()
    output_folder.mkdir(exist_ok=True, parents=True)

    config = get_config_by_type(ConfigType.SIMULATED_DATA)

    generate_simulation_experiments_service(config, output_folder)

    if not no_ethnics:
        ethnics_config = EthniCSConfig.from_json(ethnics_config_file)
        calculate_ethnics_results_service(config, ethnics_config, output_folder)

    if not no_stats:
        calculate_solvers_stats(output_folder, config)

def generate_real_data_experiments(ethnicity_file_path:Path='./data/1000g_ethnicities.csv', output_folder:Path='./read_data_output', no_ethnics:bool=False, no_stats:bool=False, ethnics_config_file:Path='./EthniCS_config.json'):
    """
    Generate real data experiments based on the given configuration type and solve it with EthniCS.

    Args:
        ethnicity_file_path (Path, optional): The file path of the ethnicity data. Defaults to './data/1000g_ethnicities.csv'.
        output_folder (Path, optional): The output folder to save the real data experiments. Defaults to './read_data_output'.
        no_ethnics (bool, optional): Flag to indicate whether to skip calculating EthniCS results. Defaults to False.
        no_stats (bool, optional): Flag to indicate whether to skip calculating solver statistics. Defaults to False.
        ethnics_config_file (Path, optional): The path to the EthniCS configuration file. Defaults to './EthniCS_config.json'.
    """
    output_folder = Path(output_folder).absolute()
    output_folder.mkdir(exist_ok=True, parents=True)

    ethnicity_file_path = Path(ethnicity_file_path).absolute()

    config = get_config_by_type(ConfigType.REAL_DATA)
    ethnicities_df = pd.read_csv(ethnicity_file_path).set_index('sample')

    generate_real_data_experiments_service(ethnicities_df, config=config, output_folder=output_folder)

    if not no_ethnics:
        ethnics_config = EthniCSConfig.from_json(ethnics_config_file)
        calculate_ethnics_results_service(config, ethnics_config, output_folder)

    if not no_stats:
        calculate_solvers_stats(output_folder, config)

def generate_super_population_experiments(ethnicity_file_path:Path='./data/1000g_super_pop_ethnicities.csv', output_folder:Path='./super_population_output', no_ethnics:bool=False, no_stats:bool=False, ethnics_config_file:Path='./EthniCS_config.json'):
    """
    Generate super population experiments based on the given configuration type and solve it with EthniCS.

    Args:
        ethnicity_file_path (Path, optional): The file path of the ethnicity data. Defaults to './data/1000g_super_pop_ethnicities.csv'.
        output_folder (Path, optional): The output folder to save the real data experiments. Defaults to './super_population_output'.
        no_ethnics (bool, optional): Flag to indicate whether to skip calculating EthniCS results. Defaults to False.
        no_stats (bool, optional): Flag to indicate whether to skip calculating solver statistics. Defaults to False.
        ethnics_config_file (Path, optional): The path to the EthniCS configuration file. Defaults to './EthniCS_config.json'.
    """
    output_folder = Path(output_folder).absolute()
    output_folder.mkdir(exist_ok=True, parents=True)

    ethnicity_file_path = Path(ethnicity_file_path).absolute()

    config = get_config_by_type(ConfigType.SUPER_POPULATION)
    ethnicities_df = pd.read_csv(ethnicity_file_path)

    generate_super_population_experiments_service(ethnicities_df, config=config, output_folder=output_folder)

    if not no_ethnics:
        ethnics_config = EthniCSConfig.from_json(ethnics_config_file)
        calculate_ethnics_results_service(config, ethnics_config, output_folder)

    if not no_stats:
        calculate_solvers_stats(output_folder, config)

def calculate_experiment_statistics(experiments_folder, config_type:ConfigType=ConfigType.REAL_DATA):
    """
    Calculate statistics for the solvers using different experiment configurations.

    Args:
        experiments_folder (str): The path to the folder containing the experiment data.
        config_type (ConfigType): The type of configuration to use for calculating the statistics.
    """
    config = get_config_by_type(config_type)
    experiments_folder = Path(experiments_folder).absolute()
    calculate_solvers_stats(experiments_folder, config)

if __name__ == '__main__':
    Fire({
        'convert_iadmix_output': convert_iadmix_output,
        'calculate_ethnics_results': calculate_ethnics_results,
        'generate_simulation_experiments': generate_simulation_experiments,
        'generate_real_data_experiments': generate_real_data_experiments,
        'generate_super_population_experiments': generate_super_population_experiments,
        'calculate_experiment_statistics': calculate_experiment_statistics,
    })