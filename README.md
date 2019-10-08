# EnsembleKQC
An Unsupervised Ensemble Learning Method for Quality Control of Single Cell RNA-seq Sequencing Data

## Requirements
* Python 3
* Scikt-learn
* Numpy
* Pandas

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
Users can also provide their own range of low-quality cells number:
```bash
$ python -u runEnsembleKQC.py --input_path ./example_data/labeled_Kolodziejczyk.csv --lower_bound 96 --upper_bound 192 --labeled True --output_path ./result.csv
```

