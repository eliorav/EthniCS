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

def simulate_diff_domain(
    domain: BaseTransformer,
    transformers: List[BaseTransformer],
    solvers: List[CsSolver],
    n,
    m,
    metrics: Optional[List[Metric]] = [],
    max_k=5,
    should_search_params=False,
):
    """
    Simulate a compressed sensing problem from a particular domain.

    Args:
        domain (BaseTransformer): The domain to test.
        transformers (List[BaseTransformer]): A list of transformations to check.
        solvers (List[CsSolver]): A list of solvers to use.
        n (int): The size of the vector.
        m (int): The number of measurements.
        metrics (Optional[List[Metric]], optional): A list of metrics to collect. Defaults to [].
        max_k (int, optional): The maximum number of non-zero elements in the vector. Defaults to 5.
        should_search_params (bool, optional): Whether to use hyperparameter optimization for the solvers. Defaults to False.

    Returns:
        tuple: A tuple containing the data for the original and reconstructed vectors, the metrics results, and the sensing matrix.
    """

    phi = generate_bernoulli_matrix(n, m)
    x, a, k = generate_random_vector(n, max_k, domain)
    y = get_sensing_vector(phi, x)

    solvers_data = get_solvers_results(
        phi, y, transformers, solvers, should_search_params
    )
    x_ethnics = get_ethnics_solution(phi, y, solvers_data, threshold=0.7)

    data_x = {"x": x, "ethnics": x_ethnics}
    for key, val in solvers_data.items():
        data_x[f"{key[0]}-{key[1]}"] = val[0]

    data_a = {"a": a}
    for key, val in solvers_data.items():
        data_a[f"{key[0]}-{key[1]}"] = val[1]

    metrics_res = []

    sol_metrics_data = {
        "name": f"ethnics",
    }

    for metric in metrics:
        sol_metrics_data[metric.get_title()] = metric(
            a,
            domain.transform_vector(x_ethnics),
            x,
            x_ethnics,
            y,
            get_sensing_vector(phi, x_ethnics),
        )
    metrics_res += [sol_metrics_data]

    for sol_name, sol_data in solvers_data.items():
        sol_metrics_data = {
            "name": f"{sol_name[1]}-{sol_name[0]}",
        }

        for metric in metrics:
            sol_metrics_data[metric.get_title()] = metric(
                a, sol_data[1], x, sol_data[0], y, sol_data[2]
            )
        metrics_res += [sol_metrics_data]

    return data_x, data_a, metrics_res, phi