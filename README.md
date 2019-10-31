# EnsembleKQC
An Unsupervised Ensemble Learning Method for Quality Control of Single Cell RNA-seq Sequencing Data

## Requirements
* Python 3
* Scikt-learn
* Numpy
* Pandas

## Preprocessing
EnsembleKQC use following five features to detect low-quality cells:
1. Actb TPM expression
2. Gadph TPM expression
3. Metabolic process genes' TPM expression
4. The number of detected genes
5. Mapping rate

Users need to first extract these values and store them in a csv file which is similar to those in the example_data directory before run EnsembleKQC. 

We also provide a simple code to extract features:
```bash
$ python extractFeatures.py <your_expression_matrix_csv> <output_filename>
```
Here the expression matrix is a Genes X Cells FPKM or UMI matrix. Rownames are Gene names and column names are cell samples names. Note this code only extract first four features. If mapping rate of your dataset is provided, fulfill this feature using the real mapping rate, or just add a column called "Mapping rate" in the csv file and set all values in this column as 1.
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
$ python -u runEnsembleKQC.py --input_path ./example_data/Kolodziejczyk.csv --labeled False --output_path ./result.csv

$ python -u runEnsembleKQC.py --input_path ./example_data/labeled_Kolodziejczyk.csv --labeled True --output_path ./result.csv
```
Users can also provide their own estimated range of low-quality cells number:
```bash
$ python -u runEnsembleKQC.py --input_path ./example_data/labeled_Kolodziejczyk.csv --lower_bound 96 --upper_bound 192 --labeled True --output_path ./result.csv
```

