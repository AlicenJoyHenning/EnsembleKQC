import sys
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python extractFeatures.py <your_expression_matrix_csv> <output_filename> <organism> [normalize]")
        sys.exit()
    else:
        file_name = sys.argv[1]
        out_file_name = sys.argv[2]
        organism = sys.argv[3].lower()
        normalize = True if len(sys.argv) == 4 else sys.argv[4].lower() == 'true'
        print('Extracting features from', file_name, 'for organism', organism, 'with normalization', normalize)


    df = pd.read_csv(file_name, index_col = 0)
    df = df.fillna(0)

    # Normalization if specified
    if normalize:
        df = df.apply(lambda x: x / sum(x))

    # Retrieve organism-specific features
    if organism == 'mouse':
        Actb = df.loc['Actb', :]
        Gapdh = df.loc['Gapdh', :]
        metabolic_genes_file = "./gene_names/mouse_metabolic_process_genes.txt"
    elif organism == 'human':
        Actb = df.loc['ACTB', :]
        Gapdh = df.loc['GAPDH', :]
        metabolic_genes_file = "./gene_names/human_metabolic_process_genes.txt"
    else:
        print("Invalid organism. Please specify 'human' or 'mouse'.")
        sys.exit()

    with open(metabolic_genes_file, "r") as f:
        metabolic_genes = [line.strip() for line in f.readlines()]
    Metabolic_process = df.loc[metabolic_genes, :].apply(sum, axis = 0)
   
    # Extract the number of detected genes
    Detected_gene_num = df.apply(lambda col: sum(col>0), axis = 0)
    features = pd.DataFrame(
        data = {
                'Actb': Actb,
                'Gapdh': Gapdh,
                'Metabolic process': Metabolic_process,
                '#Detected Genes': Detected_gene_num
            },
            index = df.columns
    )
    features.to_csv(out_file_name, columns = ["Actb", "Gapdh", "Metabolic process", "#Detected Genes"])
    print("Stored results in", out_file_name)