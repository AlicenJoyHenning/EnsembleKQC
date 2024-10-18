# EnsembleKQC
An Unsupervised Ensemble Learning Method for Quality Control of Single Cell RNA-seq Sequencing Data

## Requirements
* Python 3
* Scikit-learn
* Numpy
* Pandas

## Preprocessing
EnsembleKQC uses the following five features to detect low-quality cells:
1. Actb TPM expression
2. Gapdh TPM expression
3. Metabolic process genes' TPM expression
4. The number of detected genes
5. Mapping rate

Users need to first extract these values and store them in a CSV file similar to those in the `example_data` directory before running EnsembleKQC.

We also provide a simple code to extract features with parameters for the organism of interest and whether to perform normalization (recommended but accounting for if a user may already have normalized counts).

```bash
# Basic usage with normalization (default)
$ python extractFeatures.py file_name=./example_data/expression_matrix.csv out_file_name=./output_data/features.csv organism=human

```
Here the expression matrix is a Genes X Cells FPKM or UMI matrix. Row names are gene names and column names are cell sample names. Note this code only extracts the first four features. If the mapping rate of your dataset is provided, fulfill this feature using the real mapping rate, or just add a column called "Mapping rate" in the CSV file and set all values in this column as 1.

## Usage
Download all files and run following command to display help message

```bash
$ python runEnsembleKQC.py --help
```
```
usage: runEnsembleKQC.py [-h] [--input_path INPUT_PATH]
                         [--lower_bound LOWER_BOUND]
                         [--upper_bound UPPER_BOUND] [--labeled LABELED]
                         [--output_path OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH
                        path of input data
  --lower_bound LOWER_BOUND
                        lower bound of estimated low-quality cells number
  --upper_bound UPPER_BOUND
                        upper bound of estimated low-quality cells number
  --labeled LABELED     whether the data has quality labels. If true,
                        evaluation information will be printed
  --output_path OUTPUT_PATH
                        path of output data
```
## Example
To simply run EnsembleKQC without any prior knowledge:

```bash

# 1. Basic usage with example data
$ python runEnsembleKQC.py --input_path=./example_data/Kolodziejczyk.csv --labeled=true --output_path=./output_data/results.csv
```

Users can also provide their own estimated range of low-quality cells number:
```bash
$ python runEnsembleKQC.py --input_path=./example_data/Kolodziejczyk.csv --lower_bound=10 --upper_bound=50 --labeled=true --output_path=./output_data/results.csv
```

