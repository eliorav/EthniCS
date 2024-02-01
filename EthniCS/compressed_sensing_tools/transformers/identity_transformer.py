import numpy as np
from .base_transformer import BaseTransformer

class Transformer(BaseTransformer):
    __doc__ = BaseTransformer.__doc__

    def get_transform_matrix(self, size):
        return np.eye(size)

    def get_inverse_transform_matrix(self, size):
        return np.eye(size)

    def get_name(self):
        return "identity"
