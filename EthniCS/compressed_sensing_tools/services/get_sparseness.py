import numpy as np

def get_sparseness(x, limit=0.01):
    """
    Returns the number of non-zero elements
    """
    return np.mean(np.sum(np.abs(x) <= limit)) + 0.0
