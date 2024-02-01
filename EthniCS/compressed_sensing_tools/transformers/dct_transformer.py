import numpy as np
import scipy.fftpack as spfft
from .base_transformer import BaseTransformer

class DCTTransformer(BaseTransformer):
    __doc__ = BaseTransformer.__doc__

    def get_transform_matrix(self, size):
        return spfft.dct(np.eye(size), norm="ortho", axis=0)

    def get_inverse_transform_matrix(self, size):
        return spfft.idct(np.eye(size), norm="ortho", axis=0)

    def get_name(self):
        return "DCT"
