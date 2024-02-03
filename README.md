
# EthniCS - Large-Scale Ethnicity Screening Using Whole Genome Sequencing

## Overview
EthniCS combines whole genome sequencing and non-adaptive group testing for large-scale ethnicity screens. This project provides tools for iAdmix calculation, data conversion, result calculation, experiment generation, and statistics analysis.

## Prerequisites
Before using EthniCS, you need to prepare your data:
1. **iAdmix allele frequencies table:** Create this table following the instructions in [population_genotype_frequency/README.md](./population_genotype_frequency/README.md).
2. **Data preparation pipeline:** Execute the data preparation steps as detailed in [data_preparation/README.md](./data_preparation/README.md).
3. **Convert iAdmix Output:** Use the CLI to convert iAdmix output into a single CSV file. Instructions are provided below in the usage section.

> [!TIP]
> For a quicker start, you may use the sample data provided in `data/1000g_ethnicities.csv` or `data/1000g_super_pop_ethnicities.csv`.

## Installation
Set up EthniCS with the following steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/eliorav/EthniCS.git
   cd EthniCS
   ```

2. **Sync and update submodules:**
   ```bash
   git submodule init
   git submodule update --recursive --remote
   ```

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## EthniCS CLI (run.py)

This command-line interface (CLI) is designed for the EthniCS project to facilitate various operations including data conversion, result calculation, experiment generation, and statistics analysis.

### Usage

#### Convert iAdmix Output

Convert iAdmix output files to a CSV format:

```bash
python run.py convert_iadmix_output --iadmix_output_folder=<PATH_TO_IADMIX_OUTPUT> --output_folder=<OUTPUT_FOLDER>
```

#### Calculate EthniCS Results

Calculate EthniCS results for a specified configuration:

```bash
python run.py calculate_ethnics_results --config_type=<CONFIG_TYPE> --output_folder=<OUTPUT_FOLDER> --ethnics_config_file=<ETHNICS_CONFIG_FILE>
```

#### Generate Simulation Experiments

Generate simulation experiments with optional EthniCS result calculation and solver statistics:

```bash
python run.py generate_simulation_experiments --output_folder=<OUTPUT_FOLDER> --no_ethnics=<True/False> --no_stats=<True/False> --ethnics_config_file=<ETHNICS_CONFIG_FILE>
```

#### Generate Real Data Experiments

Generate real data experiments using specified ethnicity data, with optional EthniCS result calculation and solver statistics:

```bash
python run.py generate_real_data_experiments --ethnicity_file_path=<ETHNICITY_FILE_PATH> --output_folder=<OUTPUT_FOLDER> --no_ethnics=<True/False> --no_stats=<True/False> --ethnics_config_file=<ETHNICS_CONFIG_FILE>
```

#### Generate Super Population Experiments

Generate super population experiments with optional EthniCS result calculation and solver statistics:

```bash
python run.py generate_super_population_experiments --ethnicity_file_path=<ETHNICITY_FILE_PATH> --output_folder=<OUTPUT_FOLDER> --no_ethnics=<True/False> --no_stats=<True/False> --ethnics_config_file=<ETHNICS_CONFIG_FILE>
```

#### Calculate Experiment Statistics

Calculate statistics for experiments based on the specified configuration:

```bash
python run.py calculate_experiment_statistics --experiments_folder=<EXPERIMENTS_FOLDER> --config_type=<CONFIG_TYPE>
```


Replace `<CONFIG_TYPE>` with the appropriate configuration type (`real_data`, `simulated_data`, or `super_population`), `<OUTPUT_FOLDER>` with the path to save results, and `<ETHNICS_CONFIG_FILE>` with the path to the EthniCS configuration file.