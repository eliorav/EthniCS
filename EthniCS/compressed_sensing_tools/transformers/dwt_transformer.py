import math
import numpy as np
from .base_transformer import BaseTransformer

class DWTTransformer(BaseTransformer):
    __doc__ = BaseTransformer.__doc__

    def get_transform_matrix(self, size):
        ih = np.zeros((size, size))
        ih[0, :] = 1 / math.sqrt(size)
        for k in range(1, size):
            p = np.fix(math.log(k) / math.log(2))
            k1 = 2 ** p
            k2 = 2 ** (p + 1)
            q = int(k - k1)
            t1 = int(size / k1)
            t2 = int(size / k2)

            for i in range(t2):
                ih[k, i + q * t1] = (2 ** (p / 2)) / math.sqrt(size)
                ih[k, i + q * t1 + t2] = -(2 ** (p / 2)) / math.sqrt(size)
        return ih

    def get_inverse_transform_matrix(self, size):
        return np.linalg.inv(self.get_transform_matrix(size))

    def get_name(self):
        return "DWT"