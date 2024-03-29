from ..compressed_sensing_tools.solvers import *
from ..compressed_sensing_tools.transformers import *
from .base_config import BaseConfig
from typing import List
import numpy as np

class SimulationDataConfig(BaseConfig):
    selected_solvers:List[CsSolver] = [
        OMPSolver,
        CoSaMPSolver,
        FISTASolver,
        GPSRBBSolver,
        SCSSolver,
        ISTASolver,
    ]
    selected_transformers:List[BaseTransformer] = [Transformer(), DCTTransformer(), DWTTransformer()]
    sparsity_ratios:np.array = np.arange(0.01, 0.2, 0.01)