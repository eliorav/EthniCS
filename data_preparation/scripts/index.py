import argparse
from pathlib import Path
import subprocess
from config import SORTED_FOLDER, LOAD_SAMTOOL

def index(args):
    '''
    create an index file for the pools

    Args:
        args (argparse.Namespace): The command-line arguments.

    '''
    output_folder = Path(args.output_folder)
    sorted_folder = output_folder/SORTED_FOLDER
    input_file = sorted_folder/f'pool_{args.pool_idx}.sort.bam'

    command = f"{LOAD_SAMTOOL} samtools index {input_file}"
    subprocess.getoutput(command) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="sort the pool file.")
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
    args = parser.parse_args()

    index(args)