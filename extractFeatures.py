import sys
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python extractFeatures.py <your_expression_matrix_csv> <output_filename>")
        sys.exit();
    else:
        file_name = sys.argv[1]
        out_file_name = sys.argv[2]
        print('Extracting features from', file_name)

    df = pd.read_csv(file_name, index_col = 0)
    df = df.fillna(0)
    # Normalization
    df = df.apply(lambda x: x / sum(x))
    # Extract Actb, Gadph, Metabolic process genes expression
    Actb = df.loc['Actb', :]
    Gadph = df.loc['Gapdh', :]
    with open("./gene_names/metabolic_process_genes.txt", "r") as f:
        metabolic_genes = [line.strip() for line in f.readlines()]
    Metabolic_process = df.loc[metabolic_genes, :].apply(sum, axis = 0)
    # Extract the number of detected gene
    Detected_gene_num = df.apply(lambda col: sum(col>0), axis = 0)
    features = pd.DataFrame(
                    data = {
                        'Actb': Actb,
                        'Gadph': Gadph,
                        'Metabolic process': Metabolic_process,
                        '#Detected Genes': Detected_gene_num
                    },
                    index = df.columns
            )
    features.to_csv(out_file_name, columns = ["Actb", "Gadph",
        "Metabolic process", "#Detected Genes"])
    print("Stored results in", out_file_name)
