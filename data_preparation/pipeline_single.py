import argparse
import random
from pathlib import Path
from slurm_utils import sbatch
from scripts.config import LOAD_CONDA, ACTIVATE_PYTHON


def run_script(script, output_folder, args=''):
    """
    Run a script with specified arguments and output folder.

    Args:
        script (str): The name of the script to run.
        output_folder (str): The path to the output folder.
        args (str, optional): Additional arguments for the script. Defaults to ''.

    Returns:
        str: The command to run the script.
    """
    return f"{LOAD_CONDA} {ACTIVATE_PYTHON} python scripts/{script}.py --output_folder {output_folder} {args}"


def download(args, output_folder, dep=''):
    '''
    download samples.

    Args:
        args: The command line arguments.
        output_folder (str): The path to the output folder.
        dep (str, optional): The job dependency. Defaults to ''.

    Returns:
        str: The job command.
    '''
    task = 'download'
    return sbatch(task, run_script(task, output_folder, "--sample_idx " + "${SLURM_ARRAY_TASK_ID}"), dep=dep, mem='4g', cpus_per_task=2, multiple=args.total_samples)


def cleanup(args, output_folder, dep=''):
    '''
    cleanup files.

    Args:
        args: The command line arguments.
        output_folder (str): The path to the output folder.
        dep (str, optional): The job dependency. Defaults to ''.

    Returns:
        str: The job command.
    '''
    task = 'cleanup'
    return sbatch(task, run_script(task, output_folder, "--sample_idx " + "${SLURM_ARRAY_TASK_ID}"), dep=dep, multiple=args.total_samples)


def iadmix_single(args, output_folder, allele_freq_path, dep=''):
    '''
    Calculate ethnicity of single sample.

    Args:
        args: The command line arguments.
        output_folder (str): The path to the output folder.
        dep (str, optional): The job dependency. Defaults to ''.

    Returns:
        str: The job command.
    '''
    task = 'iadmix_single'
    return sbatch(task, run_script(task, output_folder, f"--allele_freq_path {allele_freq_path} --sample_idx " + "${SLURM_ARRAY_TASK_ID}"), dep=dep, mem='4g', cpus_per_task=2, multiple=args.total_samples)


def main(args):
    """
    Main function to run the pipeline.

    Args:
        args: The command line arguments.
    """
    output_folder = Path(args.output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)
    allele_freq_path = Path(args.allele_freq_path).absolute()

    download_job = download(args, output_folder)
    iadmix_single_job = iadmix_single(args, output_folder, allele_freq_path, download_job)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates ethnicity for a single sample using iadmix.")
    parser.add_argument(
        "--allele_freq_path",
        type=str,
        help="The path to the allele frequency file",
    )
    parser.add_argument(
        "--output_folder",
        default='./output',
        help="The output folder",
    )
    parser.add_argument(
        "--total_samples",
        default=1024,
        type=int,
        help="The number of samples to download",
    )
    args = parser.parse_args()

    main(args)
