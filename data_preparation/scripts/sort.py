import argparse
from pathlib import Path
import subprocess
from config import SORTED_FOLDER, MERGED_FOLDER, LOAD_SAMTOOL

def sort(args):
    '''
    Sorts the files of the pools.

    Args:
        args (argparse.Namespace): The command line arguments.

    '''
    output_folder = Path(args.output_folder)
    temp_folder = Path(args.temp_folder)

    merged_folder = output_folder/MERGED_FOLDER
    sorted_folder = output_folder/SORTED_FOLDER
    sorted_folder.mkdir(exist_ok=True, parents=True)
    input_file = merged_folder/f'pool_{args.pool_idx}.bam'
    output_file = sorted_folder/f'pool_{args.pool_idx}.sort.bam'

    command = f"{LOAD_SAMTOOL} samtools sort -T {temp_folder} {input_file} > {output_file}; rm -rf {input_file}"
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

    sort(args)