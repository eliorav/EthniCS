# EthniCS - Data Preparation 
This folder involves scripts for downloading and preparing DNA data from the EthniCS paper.
The folder contains two main scripts: pipeline_single and pipeline.

## Dependencies 
* SLURM 
* python 2 for iAdmix
* python 3 for the main code

### Prerequisite
In order to run iAdmix, you need to compile the code: run `make all` in the iAdmix directory.
for more details about iAdmix, see iAdmix README [here](iAdmix/README.md). 

## pipeline_single.py
Downloads DNA files and calculates their ethnicity estimation.

```
usage: pipeline_single.py [-h] [--allele_freq_path ALLELE_FREQ_PATH] [--output_folder OUTPUT_FOLDER] [--total_samples TOTAL_SAMPLES]

Creates ethnicity for a single sample using iadmix.

optional arguments:
  -h, --help            show this help message and exit
  --allele_freq_path ALLELE_FREQ_PATH
                        The path to the allele frequency file
  --output_folder OUTPUT_FOLDER
                        The output folder
  --total_samples TOTAL_SAMPLES
                        The number of samples to download
```

## pipeline.py
Creates pools of DNA samples using Bernoulli sampling, merges these samples into a single file, sorts the merged DNA file, creates an index, and calculates ethnicity for each pool.

Run this script after `pipeline_single.py` script.

```
usage: pipeline.py [-h] [--allele_freq_path ALLELE_FREQ_PATH] [--output_folder OUTPUT_FOLDER] [--samples_in_pool SAMPLES_IN_POOL]
                   [--number_of_pools NUMBER_OF_POOLS] [--total_samples TOTAL_SAMPLES]

Creates ethnicity for a pool using iadmix.

optional arguments:
  -h, --help            show this help message and exit
  --allele_freq_path ALLELE_FREQ_PATH
                        The path to the allele frequency file
  --output_folder OUTPUT_FOLDER
                        The output folder
  --samples_in_pool SAMPLES_IN_POOL
                        Number of samples in the pool
  --number_of_pools NUMBER_OF_POOLS
                        The number of pools to create
  --total_samples TOTAL_SAMPLES
                        The number of samples to download
```