import argparse
from pathlib import Path
import subprocess
from config import SORTED_FOLDER, POOL_ETHNICITY_FOLDER
from iadmix_command import iadmix_command

def iadmix_pool(args):
    '''
    Calculate the ethnicity of a pool.

    Args:
        args (argparse.Namespace): Command line arguments.
    '''
    output_folder = Path(args.output_folder)

    sorted_folder = output_folder/SORTED_FOLDER
    input_file = sorted_folder/f'pool_{args.pool_idx}.sort.bam'

    output_folder = output_folder/POOL_ETHNICITY_FOLDER/f'pool_{args.pool_idx}'
    output_folder.mkdir(exist_ok=True, parents=True)

    command = iadmix_command(input_file, output_folder, args.allele_freq_path, args.samples_in_pool)
    subprocess.getoutput(command) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge the samples into a pool.")
    parser.add_argument(
        "--output_folder",
        help="The output folder",
    )
    parser.add_argument(
        "--temp_folder",
        help="The temp folder",
    )
    parser.add_argument(
        "--pool_idx",
        type=int,
        help="The index of the current pool",
    )
    parser.add_argument(
        "--samples_in_pool",
        type=int,
        help="Number of samples in the pool",
    )
    parser.add_argument(
        "--allele_freq_path",
        type=str,
        help="The path to the allele frequency file",
    )
    args = parser.parse_args()

    iadmix_pool(args)