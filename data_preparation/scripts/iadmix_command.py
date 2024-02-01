from config import LOAD_CONDA, ACTIVATE_PYTHON2

def iadmix_command(bam, output, allele_freq_path, pool_size=1):
    '''
    Generate the iAdmix command for calculating ethnicity of a pool or single sample.

    Args:
        bam (str): Path to the BAM file.
        output (str): Path to the output folder.
        allele_freq_path (str): Path to the allele frequency file.
        pool_size (int, optional): Number of samples in the pool. Defaults to 1.

    Returns:
        str: The iAdmix command.
    '''
    return f"{LOAD_CONDA} {ACTIVATE_PYTHON2} python iAdmix/runancestry.py --path iAdmix/ -f {allele_freq_path} --bam {bam} -o {output}/ethnicity -p {pool_size}"
