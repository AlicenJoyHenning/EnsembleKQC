# EnsembleKQC
An Unsupervised Ensemble Learning Method for Quality Control of Single Cell RNA-seq Sequencing Data

## Requirements
* ```Python```, the base language for this package. 
* Libraries: ```Scikit-learn```, ```Numpy```, and ```Pandas```.
* Standard libraries: ```multiprocessing```, ```argparse```, ```itertools```, and ```time```.

## Preprocessing
EnsembleKQC uses the following five features to detect low-quality cells:
1. Actin Beta (ACTB) TPM expression
2. Glyceraldehyde-3-Phosphate Dehydrogenase (GAPDH) TPM expression
3. Metabolic process genes' TPM expression
4. The number of detected genes
5. Mapping rate

<br>

Users need to first extract these values and store them in a CSV file similar to those in the `example_data` directory before running ```EnsembleKQC```. We provide a simple code to extract features with parameters for the organism of interest:

```bash

$ python extractFeatures.py file_name=./example_data/expression_matrix.csv out_file_name=./output_data/features.csv organism=human

```
>
> NB: User can specify not to perform normalization if it has been done prior, --normalize=false
> 

Here the expression matrix is a Genes X Cells FPKM or UMI matrix. Row names are gene names and column names are cell sample names. Note this code only extracts the first four features. If the mapping rate of your dataset is provided, fulfill this feature using the real mapping rate, or just add a column called "Mapping rate" in the CSV file and set all values in this column as 1.

## Usage
Clone this repository and run following command to display help message

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
To test ```EnsembleKQC``` installation, two examples have been provided within this repository.

<br>

The first example uses a count matrix (CSV) as input, runs the [extractFeatures](https://github.com/AlicenJoyHenning/EnsembleKQC/blob/master/extractFeatures.py)

```bash
cd EnsembleKQC/
mkdir outputs # recommended to create folder for output storage

# Run the script to extract features
python extractFeatures.py ./example_data/matrix_data.csv ./outputs/matrix_extractedFeatures.csv human --normalize=true
# Check that this output is identical to that in ./example_data/matrix_extractedFeatures.csv

# Use the features to run main, labeling function
 python ./runEnsembleKQC.py --input_path=./outputs/matrix_extractedFeatures.csv --labeled=false --output_path=./outputs/matrix_results.csv
# Check that this output is identical to that in ./example_data/matrix_results.csv
```

<br>

The output format of runEnsembleKQC.py is a csv with cell identifiers and damaged cell labels that can be used to filter your sample. 
> GGCTCGACATCTACGA,damaged <br>
> GCGACCAAGAATCTCC,cell <br>
> GGAATAATCTTAACCT,cell

<br>
<br>

Another example is provided where pre-calculated features are used as input for runEnsembleKQC and damaged labels are included.
```bash
# Using input csv
 python ./runEnsembleKQC.py --input_path=./example_data/labeled_Kolodziejczyk.csv --labeled=true --output_path=./outputs/Kolodziejczyk_results.csv
# Check that this output is identical to that in ./example_data/Kolodziejczyk_results.csv
```

Users can also provide their own estimated range of low-quality cells number:
```bash
$ python runEnsembleKQC.py --input_path=./example_data/Kolodziejczyk.csv --lower_bound=10 --upper_bound=50 --labeled=true --output_path=./outputs/results.csv
```

