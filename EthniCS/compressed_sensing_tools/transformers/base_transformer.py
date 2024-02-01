from abc import ABC

class BaseTransformer(ABC):
    """
    A base class for a transformer
    """

    def get_transform_matrix(self, size):
        """
        Returns the transformation matrix
        param size: the size of the matrix
        """

    def get_inverse_transform_matrix(self, size):
        """
        Returns the inverse of the transformation matrix
        param size: the size of the matrix
        """

    def get_name(self):
        """
        Returns the name of the transformation
        """

    def transform_vector(self, x):
        """
        Transform the vector to Transformer doamin
        """
        return self.get_transform_matrix(x.size) @ x

    def inverse_transform_vector(self, a):
        """
        Transform the vector back from the Transformer doamin
        """
        return self.get_inverse_transform_matrix(a.size) @ a