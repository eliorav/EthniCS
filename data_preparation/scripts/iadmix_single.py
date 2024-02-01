import argparse
from pathlib import Path
import subprocess
import shutil
import pandas as pd
from config import DOWNLOAD_FOLDER, LIST_PATH, SINGLE_ETHNICITY_FOLDER
from iadmix_command import iadmix_command

def iadmix_single(args):
    '''
    Calculate the ethnicity of a single sample.

    Args:
        args (argparse.Namespace): The command line arguments.
    '''
    try:
        output_folder = Path(args.output_folder)
        download_folder = output_folder/DOWNLOAD_FOLDER

        df = pd.read_csv(LIST_PATH)
        sample_info = df.iloc[args.sample_idx-1]
        sample_folder = download_folder/sample_info['ethnicity']/sample_info['name']

        print(sample_folder)
        print(list(sample_folder.rglob('*.bam')))
        input_file = list(sample_folder.rglob('*.bam'))[0]

        output = output_folder/SINGLE_ETHNICITY_FOLDER/input_file.parent.name
        output.mkdir(exist_ok=True, parents=True)

        command = iadmix_command(input_file, output, args.allele_freq_path, pool_size=1)
        subprocess.getoutput(command) 
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="merge the samples into pool.")
    parser.add_argument(
        "--output_folder",
        help="The output folder",
    )
    parser.add_argument(
        "--sample_idx",
        type=int,
        help="The index of the current pool",
    )
    parser.add_argument(
        "--allele_freq_path",
        type=str,
        help="The path to the allele frequency file",
    )
    args = parser.parse_args()
    print(args)

    iadmix_single(args)