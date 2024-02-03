import numpy as np

def generate_random_ethnicity_vector(p, n):
    """
    Generate a random ethnicity vector based on the given probability distribution.

    Parameters:
    p (list): The probability distribution of ethnicities.
    n (int): The length of the vector.

    Returns:
    list: A random ethnicity vector.
    """
    res = []
    
    for _ in range(n):
        value = np.random.choice(np.arange(0, 1, 0.05), p=p)
        res += [0 if value == 0 else np.random.uniform(value,value+0.051)]
        
    return res


def generate_ethnicity_matrix(ethnicity_distribution, n):
    """
    Returns an ethnicity matrix from the given ethnicity distribution.

    Parameters:
    ethnicity_distribution (dict): The distribution of ethnicities.
    n (int): The number of vectors in the matrix.

    Returns:
    numpy.ndarray: An ethnicity matrix.
    """
    return np.array([generate_random_ethnicity_vector(ethnicity_distribution[i], n) for i in ethnicity_distribution.keys()]).T