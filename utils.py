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
    with open(file_name, "r") as f:
        lines = f.readlines()
    lines = lines[1:]
    col = len(list(lines[0].split(','))) - 1
    label = []
    mat = []
    for i in range(col - 1):
        mat.append([])
    for l in lines:
        for i, val in enumerate(l.strip().split(',')[1:]):
            if i == col - 1:
                label.append(int(val))
            else:
                mat[i].append(float(val))
    return mat, label

def load_features(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    lines = lines[1:]
    col = len(list(lines[0].split(','))) - 1
    mat = []
    for i in range(col):
        mat.append([])
    for l in lines:
        for i, val in enumerate(l.strip().split(',')[1:]):
            mat[i].append(float(val))
    return mat
