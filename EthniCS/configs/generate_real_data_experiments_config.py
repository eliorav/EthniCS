from ..compressed_sensing_tools.solvers import *
from ..compressed_sensing_tools.transformers import *
from .base_config import BaseConfig
from typing import List

class RealDataConfig(BaseConfig):
    # selected_solvers:List[CsSolver] = [
    #     OMPSolver,
    #     CoSaMPSolver,
    #     FISTASolver,
    #     GPSRBBSolver,
    #     SCSSolver,
    #     ISTASolver,
    # ]
    # selected_transformers:List[BaseTransformer] = [Transformer(), DCTTransformer(), DWTTransformer()]
    selected_solvers:List[CsSolver] = [
        OMPSolver,
        CoSaMPSolver,
    ]
    selected_transformers:List[BaseTransformer] = [Transformer()]
    number_of_pools_range:List[int] = list(range(256, 513, 64))
    number_of_individuals:int = 1024
    num_of_exp: int = 1
    should_search_params:bool = False # Whether to search for the best parameters for the solvers or not