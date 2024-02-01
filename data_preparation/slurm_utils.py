import subprocess

def sbatch(job_name, command, log_folder='./logs', mem='2g', cpus_per_task=1, multiple=None, dep=''): 
    """
    Submit a job to SLURM using the sbatch command.

    Args:
        job_name (str): The name of the job.
        command (str): The command to be executed by the job.
        log_folder (str, optional): The folder to store the job logs. Defaults to './logs'.
        mem (str, optional): The memory allocation for the job. Defaults to '2g'.
        cpus_per_task (int, optional): The number of CPUs per task for the job. Defaults to 1.
        multiple (int, optional): The number of job array tasks. Defaults to None.
        dep (str, optional): The job dependency ID. Defaults to ''.

    Returns:
        str: The ID of the submitted job.
    """
    if dep != '': 
        dep = f'--dependency=afterok:{dep} --kill-on-invalid-dep=yes '

    sbatch_command = f"sbatch -J {job_name} -o {log_folder}/{job_name}.out -e {log_folder}/{job_name}.err --mem={mem} --cpus-per-task={cpus_per_task} --wrap='{command}' {dep}"

    if multiple is not None:
        sbatch_command = f'{sbatch_command} --array=1-{multiple}%{min(multiple, 5)}'

    sbatch_response = subprocess.getoutput(sbatch_command) 
    print(sbatch_response) 

    job_id = sbatch_response.split(' ')[-1].strip() 
    return job_id