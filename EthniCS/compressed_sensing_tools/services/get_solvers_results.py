import itertools
from multiprocessing import Pool, cpu_count
import numpy as np
from .cs_runner import CSRunner


def get_solvers_results(
    phi, y, transformers, solvers, should_search_params, parallel=False
):
    """
    Solve the CS problem for a multiple solvers and transformers.
    Can run in parallel
    """
    cs_runner = CSRunner(phi, y, should_search_params)

    if parallel:
        with Pool(int(cpu_count() / 2)) as p:
            results = p.map(cs_runner, itertools.product(solvers, transformers))
    else:
        results = map(cs_runner, itertools.product(solvers, transformers))
    return {name: res for name, res in results}
