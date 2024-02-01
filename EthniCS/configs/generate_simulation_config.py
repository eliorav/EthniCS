from ..compressed_sensing_tools.solvers import *
from ..compressed_sensing_tools.transformers import *
from .base_config import solvers_results_name, x_ethnics_filename, similar_solvers

selected_solvers = [
    OMPSolver,
    CoSaMPSolver,
    FISTASolver,
    GPSRBBSolver,
    SCSSolver,
    ISTASolver,
]
selected_transformers = [Transformer(), DCTTransformer(), DWTTransformer()]
number_of_pools_range = range(64, 513, 64)
