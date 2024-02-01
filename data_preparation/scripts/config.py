from pathlib import Path

DOWNLOAD_FOLDER = 'download'
MERGED_FOLDER = 'merged'
SORTED_FOLDER = 'sorted'
METADATA_FOLDER = 'metadata'
SINGLE_ETHNICITY_FOLDER = 'ethnicity_single'
POOL_ETHNICITY_FOLDER = 'ethnicity_pool'

LIST_PATH = Path('phase3_ftp_list.csv').absolute()

LOAD_CONDA = 'module load anaconda3;'
LOAD_SAMTOOL = 'module load samtools/1.10;'
ACTIVATE_PYTHON = 'source activate elior_env;'
ACTIVATE_PYTHON2 = 'source activate elior_env_2.7;'

FTP_PROXY = 'http://proxy.cslab.openu.ac.il:80'
DATA_FTP_SERVER = 'ftp://ftp.1000genomes.ebi.ac.uk'