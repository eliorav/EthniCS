import argparse
from pathlib import Path
import random
import pandas as pd
import subprocess
from config import DOWNLOAD_FOLDER, MERGED_FOLDER, METADATA_FOLDER, LOAD_SAMTOOL

def merge(args):
    '''
    merge the samples into one pool

    Args:
        args (argparse.Namespace): The command line arguments.
    '''
    output_folder = Path(args.output_folder)

    download_folder = output_folder/DOWNLOAD_FOLDER
    merged_folder = output_folder/MERGED_FOLDER
    merged_folder.mkdir(exist_ok=True, parents=True)
    metadata_folder = output_folder/METADATA_FOLDER
    metadata_folder.mkdir(exist_ok=True, parents=True)

    output_file = merged_folder/f'pool_{args.pool_idx}.bam'

    samples = list(download_folder.rglob('*.bam'))
    selected_samples = random.choices(samples, k=args.samples_in_pool)
    selected_samples_string = " ".join(map(str, selected_samples))

    # Save as metadata the samples that were selected for the pool
    pd.DataFrame([p.parent.name for p in selected_samples]).to_csv(metadata_folder/f'pool_{args.pool_idx}.csv')

    command = f"{LOAD_SAMTOOL} samtools merge {output_file} {selected_samples_string}"
    subprocess.getoutput(command) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="merge the samples into pool.")
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
    args = parser.parse_args()

    merge(args)