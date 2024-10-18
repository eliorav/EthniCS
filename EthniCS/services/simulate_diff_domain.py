import numpy as np
import pandas as pd
from typing import Optional, List
from ..compressed_sensing_tools.sensing_matrix import generate_bernoulli_matrix
from ..compressed_sensing_tools.services import get_sensing_vector, get_solvers_results, get_ethnics_solution
from ..compressed_sensing_tools.transformers import BaseTransformer
from ..compressed_sensing_tools.solvers import CsSolver
from ..compressed_sensing_tools.metrics import Metric

def generate_random_vector(n, max_k, domain: BaseTransformer):
    """
    Generate a random vector of size n for a given domain.

    Args:
        n (int): The size of the vector.
        max_k (int): The maximum number of non-zero elements in the vector.
        domain (BaseTransformer): The domain to generate the vector for.

    Returns:
        tuple: A tuple containing the generated vector, its transformed representation, and the number of non-zero elements.
    """
    a = np.zeros(n)
    k = np.random.choice(range(1, max_k + 1))
    a[np.random.choice(range(n), k)] = np.random.uniform(0, 1, k)
    x = domain.inverse_transform_vector(a)
    x[x < 0] = 0
    return x, domain.transform_vector(x), k