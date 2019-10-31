import pandas as pd
def calc_pre_recall_F1(pred, truth):
    precision = 0
    recall = 0
    P = 0
    TP = 0
    low_quality_cnt = 0
    for i in range(len(pred)):
        if pred[i] == 0:
            P += 1
            if truth[i] == 0:
                TP += 1
        if truth[i] == 0:
            low_quality_cnt += 1
    precision = TP / P
    recall = TP / low_quality_cnt
    F1 = 2*precision*recall / (precision + recall)
    return precision, recall, F1

def load_features_and_labels(file_name):
    csv = pd.read_csv(file_name, index_col=0)
    # If the csv file has a column named Quality, we use that column as labels
    # Otherwise the last column will be used as labels by default
    if 'Quality' in csv.columns:
        label = list(map(int, csv['Quality'].tolist()))    
        csv.drop('Quality', axis=1, inplace=True)
    else:
        label = list(map(int, csv.iloc[:, -1].tolist()))
        csv.drop(csv.columns[len(csv.columns)-1], axis=1, inplace=True)
    feature_matrix = csv.T.values.tolist()
    return feature_matrix, label

def load_features(file_name):
    csv = pd.read_csv(file_name, index_col=0)
    feature_matrix = csv.T.values.tolist()
    return feature_matrix

# mat is a n*m matrix, perform min-max scale for each row
def min_max_scale(mat):
    n = len(mat)
    m = len(mat[0])
    mins = [min(row) for row in mat]
    maxs = [max(row) for row in mat]
    for i in range(n):
        if mins[i] == maxs[i]:
            mat[i] = [1] * m
        else:
            for j in range(m):
                mat[i][j] -= mins[i];
                mat[i][j] /= maxs[i] - mins[i];
    return mat

if __name__ == '__main__':
    mat = load_features("./example_data/Kolodziejczyk.csv")
    mat, label = load_features_and_labels(
            "./example_data/labeled_Kolodziejczyk.csv")
