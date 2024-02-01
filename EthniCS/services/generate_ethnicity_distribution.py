import pickle
import numpy as np
from pathlib import Path

def generate_ethnicity_distribution(ethnicities_df, out_folder):
    ethnicity_distribution = {}

    for ethnicity_num in range(ethnicities_df.shape[1]):
        ethnicity = ethnicities_df.values[:, ethnicity_num]

        p = []
        for i in np.arange(0, 1, 0.05):
            mask = (
                (ethnicity >= i) & (ethnicity <= i + 0.05)
                if i == 0
                else (ethnicity > i) & (ethnicity <= i + 0.05)
            )

            p += [len(ethnicity[mask]) / len(ethnicity)]
        ethnicity_distribution[ethnicity_num] = p

    with open(Path(out_folder)/"ethnicity_distribution.pkl", "wb") as f_out:
        pickle.dump(ethnicity_distribution, f_out)