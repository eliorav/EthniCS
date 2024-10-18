import json
from pydantic import BaseModel

class EthniCSConfig(BaseModel):
    """
    A class representing the configuration for EthniCS.

    Attributes:
        high_psnr_threshold (int): The high PSNR threshold.
        medium_psnr_threshold (int): The medium PSNR threshold.
        low_psnr_threshold (int): The low PSNR threshold.
        alpha (int): The alpha value for the score.
        sparseness_threshold (float): The sparseness threshold.
        fine_tune_max_iter (int): The maximum number of iterations for the fine tuning.
    """

    high_psnr_threshold:int
    medium_psnr_threshold:int
    low_psnr_threshold:int
    alpha:int
    sparseness_threshold:float
    fine_tune_max_iter:int

    @classmethod
    def from_json(cls, config_file):
        """
        Load the configuration from a JSON file.

        Args:
            config_file (str): The path to the JSON file.

        Returns:
            EthniCSConfig: An instance of EthniCSConfig loaded from the JSON file.
        """
        with open(config_file, 'r') as f:
            config = json.load(f)
            return cls(**config)
        
    def to_json(self, config_file):
        """
        Save the configuration to a JSON file.

        Args:
            config_file (str): The path to the JSON file.
        """
        with open(config_file, 'w') as f:
            json.dump(self.model_dump(), f, indent=4)