import pickle
from tqdm.auto import tqdm
from .solve_ethnics_cs_ethnicity_estimation import solve_ethnics_cs_ethnicity_estimation


def generate_ethnics_results(config, output_folder):
    similar_solvers = config.similar_solvers or []
    for f in tqdm(output_folder.glob(f"**/{config.solvers_results_name}_*.pkl")):
        m = int(f.name.split("_")[-1].split(".")[0])

        with open(f, "rb") as f_in:
            x, y, phi, solvers_data = pickle.load(f_in)
            x_res, probabilities = solve_ethnics_cs_ethnicity_estimation(phi, y, solvers_data, similar_solvers=similar_solvers)
            with open(f.parent / f"{config.x_ethnics_filename}_{str(m)}.pkl", "wb") as f_out:
                pickle.dump((x_res, probabilities), f_out)
