from enum import Enum

from .base_config import BaseConfig
from .generate_real_data_experiments_config import RealDataConfig
from .generate_simulation_config import SimulationDataConfig
from .generate_super_population_experiments_config import SuperPopulationConfig

class ConfigType(str, Enum):
    """
    Enum for the different types of configurations.
    """
    REAL_DATA = "real_data"
    SIMULATED_DATA = "simulated_data"
    SUPER_POPULATION = "super_population"

config_by_type = {
    ConfigType.REAL_DATA: RealDataConfig,
    ConfigType.SIMULATED_DATA: SimulationDataConfig,
    ConfigType.SUPER_POPULATION: SuperPopulationConfig,
}

def get_config_by_type(config_type: ConfigType) -> BaseConfig:
    config_class = config_by_type.get(config_type)

    if config_class is None:
        raise ValueError(f"Config type {config_type} is not supported.")
    
    return config_class()