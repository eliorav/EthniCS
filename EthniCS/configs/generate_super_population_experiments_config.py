import numpy as np
from ..compressed_sensing_tools.solvers import *
from ..compressed_sensing_tools.transformers import *
from .generate_real_data_experiments_config import RealDataConfig
from typing import List

class SuperPopulationConfig(RealDataConfig):
    selected_ethnicity:str = 'AFR'
    ethnicity_threshold:float = 0.1 # a sample is considered to be from the "selected_ethnicity" if it's ethnicity proportion of "selected_ethnicity" is greater than this threshold
    sparsity_ratios:np.array = np.arange(0.01, 0.11, 0.01)