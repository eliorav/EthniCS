from pydantic import BaseModel, ConfigDict
from typing import List
from ..compressed_sensing_tools.solvers.cs_solver import CsSolver
from ..compressed_sensing_tools.transformers.base_transformer import BaseTransformer

class BaseConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    solvers_results_name:str = 'solvers_res'
    x_ethnics_filename:str = 'x_ethnics'
    similar_solvers:List[str] = [('FISTA', 'ISTA')]

    selected_solvers:List[CsSolver] = []
    selected_transformers:List[BaseTransformer] = []
    number_of_pools_range:List[int] = list(range(64, 513, 64))
    number_of_individuals:int = 1024
    num_of_exp: int = 10
    should_search_params:bool = True # Whether to search for the best parameters for the solvers or not