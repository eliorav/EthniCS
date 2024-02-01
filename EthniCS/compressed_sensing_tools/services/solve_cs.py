from .get_sensing_vector import get_number_of_specimens_in_pool, get_sensing_vector
import numpy as np
from ..transformers import Transformer


def solve_cs(phi, y, solver, transformer=Transformer()):
    """
    Solves the CS problem using the given solver and the transformer
    """
    D_I = transformer.get_inverse_transform_matrix(phi.shape[1])
    A = phi @ D_I
    ahat = get_number_of_specimens_in_pool(phi) * solver(A, y)
    xhat = D_I @ ahat
    xhat[xhat < 0] = 0
    xhat[xhat > 1] = 1
    yhat = get_sensing_vector(phi, xhat)
    return (xhat, ahat, yhat)
