import pandas as pd
from tqdm.auto import tqdm
from pathlib import Path

def convert_iadmix_output(iadmix_output_folder:Path, output_folder:Path):
    """
    Convert iAdmix output files to a single CSV file.

    Args:
        iadmix_output_folder (Path): The folder containing iAdmix output files.
        output_folder (Path): The folder where the converted CSV file will be saved.
    """
    df_final = pd.DataFrame()

    for res in tqdm(iadmix_output_folder.rglob('ethnicity.ancestry.out')):
        with open(res) as f:
            lines = f.read().splitlines()
            results = lines[-2][lines[-2].find("ADMIX_PROP") + len("ADMIX_PROP"):].strip().split(' ')
            results = {res.split(':')[0]: res.split(':')[1] for res in results}

            df = pd.DataFrame.from_dict(results, orient='index').T
            df['sample'] = res.parent.name
            df_final = pd.concat([df_final, df])

    df_final = df_final.set_index('sample')
    df_final.to_csv(output_folder / 'iadmix_output.csv')
