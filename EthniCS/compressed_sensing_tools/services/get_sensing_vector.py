def get_number_of_specimens_in_pool(phi): return int(phi.sum(axis=1).mean()/2)

def get_sensing_vector(phi, x):
    return (1/get_number_of_specimens_in_pool(phi)) * phi @ x
