import numpy as np


def generate_bernoulli_matrix(n, m):
    """
    Generates Bernolli matrix where the entries are 0/1 with probablity of 0.5
    """
    phi = np.zeros((m, n))
    for row in phi:
        indices = np.random.choice(
            np.arange(row.size), replace=False, size=int(row.size / 2)
        )
        row[indices] = 1
    return phi
