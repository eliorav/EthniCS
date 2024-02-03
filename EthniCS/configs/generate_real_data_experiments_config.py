from ..compressed_sensing_tools.solvers import *
from ..compressed_sensing_tools.transformers import *
from .base_config import BaseConfig
from typing import List

class RealDataConfig(BaseConfig):
    selected_solvers:List[CsSolver] = [
        OMPSolver,
        CoSaMPSolver,
        FISTASolver,
        GPSRBBSolver,
        SCSSolver,
        ISTASolver,
    ]
    selected_transformers:List[BaseTransformer] = [Transformer(), DCTTransformer(), DWTTransformer()]