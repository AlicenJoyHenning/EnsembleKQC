import sys
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Extract features from expression matrix.")
    parser.add_argument("file_name", type=str, help="Path to the expression matrix CSV file.")
    parser.add_argument("out_file_name", type=str, help="Path to the output file where the extracted features will be saved.")
    parser.add_argument("organism", type=str, choices=["human", "mouse"], help="Organism type: 'human' or 'mouse'.")
    parser.add_argument("--normalize", type=lambda x: (str(x).lower() == 'true'), default=True, help="Whether to normalize the data (default: True).")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    file_name = args.file_name
    out_file_name = args.out_file_name
    organism = args.organism.lower()
    normalize = args.normalize

    print('Extracting features from', file_name, 'for organism', organism, 'with normalization', normalize)

    df = pd.read_csv(file_name, index_col=0)
    df = df.fillna(0)

    # Normalization if specified
    if normalize:
        df = df.apply(lambda x: x / sum(x))

    # Retrieve organism-specific features
    if organism == 'mouse':
        Actb = df.loc['Actb', :] if 'Actb' in df.index else pd.Series([0]*df.shape[1], index=df.columns)
        Gapdh = df.loc['Gapdh', :] if 'Gapdh' in df.index else pd.Series([0]*df.shape[1], index=df.columns)
        metabolic_genes_file = "./gene_names/mouse_metabolic_process_genes.txt"
    elif organism == 'human':
        Actb = df.loc['ACTB', :] if 'ACTB' in df.index else pd.Series([0]*df.shape[1], index=df.columns)
        Gapdh = df.loc['GAPDH', :] if 'GAPDH' in df.index else pd.Series([0]*df.shape[1], index=df.columns)
        metabolic_genes_file = "./gene_names/human_metabolic_process_genes.txt"
    else:
        print("Invalid organism. Please specify 'human' or 'mouse'.")
        sys.exit()

    with open(metabolic_genes_file, "r") as f:
        metabolic_genes = [line.strip() for line in f.readlines()]

    # Filter metabolic genes to only those present in the DataFrame
    present_metabolic_genes = [gene for gene in metabolic_genes if gene in df.index]

    if not present_metabolic_genes:
        print("Warning: None of the metabolic genes are present in the data.")
        Metabolic_process = pd.Series([0]*df.shape[1], index=df.columns)
    else:
        Metabolic_process = df.loc[present_metabolic_genes, :].apply(sum, axis=0)

    # Extract the number of detected genes
    Detected_gene_num = df.apply(lambda col: sum(col > 0), axis=0)
    features = pd.DataFrame(
        data={
            'Actb': Actb,
            'Gapdh': Gapdh,
            'Metabolic process': Metabolic_process,
            '#Detected Genes': Detected_gene_num
        },
        index=df.columns
    )

    # Add 'Identifier' column name to the index
    features.index.name = 'Identifier'

    # Return output csv to specified location
    features.to_csv(out_file_name, columns=["Actb", "Gapdh", "Metabolic process", "#Detected Genes"])
    print("Stored results in", out_file_name)