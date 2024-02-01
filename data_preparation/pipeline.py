import argparse
from pathlib import Path
from slurm_utils import sbatch
from scripts.config import LOAD_CONDA, ACTIVATE_PYTHON


def run_script(script, output_folder, temp_folder, args=''):
    return f"{LOAD_CONDA} {ACTIVATE_PYTHON} python scripts/{script}.py --output_folder {output_folder} --temp_folder {temp_folder} {args}"


def merge(args, output_folder, temp_folder, dep=''):
    '''
    merge the samples into one pool
    '''
    task = 'merge'
    return sbatch(task, run_script(task, output_folder, temp_folder, f'--samples_in_pool {args.samples_in_pool} '+"--pool_idx " + "${SLURM_ARRAY_TASK_ID}"), multiple=args.number_of_pools, dep=dep, mem='4g', cpus_per_task=2)


def sort(args, output_folder, temp_folder, dep=''):
    '''
    sort the files of the pools
    '''
    task = 'sort'
    return sbatch(task, run_script(task, output_folder, temp_folder, "--pool_idx " + "${SLURM_ARRAY_TASK_ID}"), multiple=args.number_of_pools, dep=dep, mem='4g', cpus_per_task=2)


def index(args, output_folder, temp_folder, dep=''):
    '''
    create an index file for the pools
    '''
    task = 'index'
    return sbatch(task, run_script(task, output_folder, temp_folder, "--pool_idx " + "${SLURM_ARRAY_TASK_ID}"), multiple=args.number_of_pools, dep=dep)


def iadmix_single(args, output_folder, temp_folder, dep=''):
    '''
    calculate ethnicity of single samples
    '''
    task = 'iadmix_single'
    return sbatch(task, run_script(task, output_folder, temp_folder, "--sample_idx " + "${SLURM_ARRAY_TASK_ID}"), dep=dep, mem='4g', cpus_per_task=2, multiple=args.total_samples)


def iadmix_pool(args, output_folder, temp_folder, allele_freq_path, dep=''):
    '''
    calculate ethnicity of a pool
    '''
    task = 'iadmix_pool'
    return sbatch(task, run_script(task, output_folder, temp_folder, f'--samples_in_pool {args.samples_in_pool} --allele_freq_path {allele_freq_path} '+"--pool_idx " + "${SLURM_ARRAY_TASK_ID}"), dep=dep, mem='6g', cpus_per_task=2, multiple=args.number_of_pools)


def main(args):
    output_folder = Path(args.output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)
    temp_folder = output_folder/'temp'
    temp_folder.mkdir(exist_ok=True, parents=True)
    allele_freq_path = Path(args.allele_freq_path).absolute()

    merge_job = merge(args, output_folder, temp_folder)
    sort_job = sort(args, output_folder, temp_folder, dep=merge_job)
    index_job = index(args, output_folder, temp_folder, dep=sort_job)
    iadmix_pool_job = iadmix_pool(args, output_folder, temp_folder, allele_freq_path, dep=index_job)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates ethnicity for a pool using iadmix.")
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
        "--samples_in_pool",
        default=512,
        help="Number of samples in the pool",
    )
    parser.add_argument(
        "--number_of_pools",
        default=256,
        type=int,
        help="The number of pools to create",
    )
    parser.add_argument(
        "--total_samples",
        default=1024,
        type=int,
        help="The number of samples to download",
    )
    args = parser.parse_args()

    main(args)
