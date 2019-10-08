from multiprocessing import Pool
import itertools
import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics.pairwise import cosine_similarity
from utils import *
from configure import FLAGS

file_name = FLAGS.input_path
lower_bound = FLAGS.lower_bound
upper_bound = FLAGS.upper_bound
result_path = FLAGS.output_path
labeled = FLAGS.labeled
if labeled:
    mat, label = load_features_and_labels(file_name)
else:
    mat = load_features(file_name)
tmat = list(zip(*mat))
similarity = cosine_similarity(tmat)
feature_num = len(mat)
cell_num = len(mat[0])

def calc_score(label):
    cnt = 0
    score = 0
    for x in range(cell_num):
        for y in range(x + 1, cell_num):
            if label[x] and label[y]:
                cnt += 1
                score += similarity[x][y]
    if cnt:
        score /= cnt
    return score

def run_single_enumeration_round(thresholds, return_pred_labels = None):
    label_vectors = [[0 if tmat[i][j] <= list(thresholds)[j] else 1 for j in range(feature_num)] for i in range(cell_num)]
    kmeans = KMeans(n_clusters=2, random_state=0).fit(label_vectors)
    # Choose the smaller cluster as low-quality
    zero_cnt = sum([x == 0 for x in kmeans.labels_])
    if zero_cnt > cell_num / 2:
        # Flip values
        pred = [x ^ 1 for x in kmeans.labels_]
    else:
        pred = kmeans.labels_
    score = calc_score(pred)
    if return_pred_labels != None:
        return_pred_labels.clear()
        return_pred_labels.extend(pred)
    return score

if __name__ == '__main__':
    print("")
    for arg in vars(FLAGS):
        print("{}={}".format(arg.upper(), getattr(FLAGS, arg)))
    print("")
    if labeled:
        low_quality_cnt = cell_num - sum(label)
        print("total={}, low-quality={}, high-quality={}".format(cell_num, low_quality_cnt,
            cell_num - low_quality_cnt))
    print("{} features, {} cells".format(feature_num, cell_num))

    start = time.time()
    sorted_feature_values = [sorted(col) for col in mat]
    # Estimate range of low-quality cells
    if not lower_bound and not upper_bound:
        lower_bound = cell_num
        upper_bound = 0
        for col in sorted_feature_values:
            clf = IsolationForest(behaviour='new', contamination='auto', 
                                random_state=0)
            values = [[col[i]] for i in range(cell_num)]
            clf.fit(values)
            y_pred = clf.predict(values)
            num = sum([1 if y != 1 else 0 for y in y_pred])
            if num > cell_num / 2:
                continue
            lower_bound = min(lower_bound, num)
            upper_bound = max(upper_bound, num)
    print('range=[{},{}]'.format(lower_bound, upper_bound))

    # Get thresholds candidate list
    step = int((upper_bound - lower_bound + 1) * 0.2)
    threshold_candidate_lists = [col[lower_bound - 1 : upper_bound: step] for col in sorted_feature_values]

    p = Pool()
    enumeration_list = list(itertools.product(*threshold_candidate_lists))
    scores = p.map(run_single_enumeration_round, enumeration_list)
    max_score_id = scores.index(max(scores))
    best_thresholds = enumeration_list[max_score_id]
    result = [] 
    run_single_enumeration_round(best_thresholds, result)
    if labeled:
        precision, recall, F1 = calc_pre_recall_F1(result, label)
        print('precision {:2f} recall {:2f} F1Score {:2f}'.format(precision, recall, F1))

    # Store the result to the output path
    if result_path:
        with open(result_path, 'w') as f:
            f.write('Quality\n')
            f.writelines('\n'.join(map(str, result)))
    end = time.time()
    print('Done. Total time: {:2f}s. Results have been stored in {}'.format(end
        - start, result_path))
