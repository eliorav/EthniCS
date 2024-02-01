import numpy as np

def generate_random_ethnicity_vector(p, n):
    res = []
    
    for _ in range(n):
        value = np.random.choice(np.arange(0, 1, 0.05), p=p)
        res += [0 if value == 0 else np.random.uniform(value,value+0.051)]
        
    return res


def generate_ethnicity_matrix(ethnicity_distribution, n):
    """
    Returns an ethnicity matrix from the give ethnicity distribution
    """
    return np.array([generate_random_ethnicity_vector(ethnicity_distribution[i], n) for i in ethnicity_distribution.keys()]).T