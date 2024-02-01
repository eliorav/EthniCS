import argparse
from pathlib import Path
import subprocess
import shutil
import pandas as pd
import shutil
from config import DOWNLOAD_FOLDER, LIST_PATH


def cleanup(args):
    '''
    Calculate the ethnicity of single samples and remove the corresponding sample folder.

    Args:
        args (argparse.Namespace): The command line arguments.
    '''
    output_folder = Path(args.output_folder)
    download_folder = output_folder/DOWNLOAD_FOLDER

    df = pd.read_csv(LIST_PATH)
    sample_info = df.iloc[args.sample_idx-1]
    sample_folder = download_folder/sample_info['ethnicity']/sample_info['name']
    print(f'cleanup {sample_folder}')
    shutil.rmtree(sample_folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge the samples into pool.")
    parser.add_argument(
        "--output_folder",
        help="The output folder",
    )
    parser.add_argument(
        "--sample_idx",
        type=int,
        help="The number of the current pool",
    )
    args = parser.parse_args()

    cleanup(args)