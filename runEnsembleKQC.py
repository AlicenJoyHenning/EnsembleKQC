from multiprocessing import Pool
import itertools
import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics.pairwise import cosine_similarity
from utils import *
import argparse
from joblib import Parallel, delayed

def parse_args():
    parser = argparse.ArgumentParser(description="Run Ensemble KQC.")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input data.")
    parser.add_argument("--lower_bound", type=int, default=None, help="Lower bound of estimated low-quality cell number.")
    parser.add_argument("--upper_bound", type=int, default=None, help="Upper bound of estimated low-quality cell number.")
    parser.add_argument("--output_path", type=str, default=None, help="Path to the output data.")
    parser.add_argument("--labeled", type=lambda x: (str(x).lower() == 'true'), default=True, help="Whether the data has quality labels. If true, evaluation information will be printed.")
    return parser.parse_args()

def calc_score(label, similarity, cell_num):
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

def run_single_enumeration_round(thresholds, tmat, feature_num, cell_num, similarity, return_pred_labels=None):
    label_vectors = np.array([[0 if tmat[i][j] <= list(thresholds)[j] else 1 for j in range(feature_num)] for i in range(cell_num)])
    kmeans = KMeans(n_clusters=2, random_state=0, n_init=10).fit(label_vectors)  # Explicitly set n_init
    # Choose the smaller cluster as low-quality
    zero_cnt = np.sum(kmeans.labels_ == 0)
    if zero_cnt > cell_num / 2:
        # Flip values
        pred = np.bitwise_xor(kmeans.labels_, 1)
    else:
        pred = kmeans.labels_
    score = calc_score(pred, similarity, cell_num)
    if return_pred_labels is not None:
        return_pred_labels.clear()
        return_pred_labels.extend(pred)
    return score

def run_enumeration_round_wrapper(args):
    thresholds, tmat, feature_num, cell_num, similarity = args
    return run_single_enumeration_round(thresholds, tmat, feature_num, cell_num, similarity)

if __name__ == '__main__':
    args = parse_args()
    file_name = args.input_path
    lower_bound = args.lower_bound
    upper_bound = args.upper_bound
    result_path = args.output_path
    labeled = args.labeled

    print("")
    for arg in vars(args):
        print("{}={}".format(arg.upper(), getattr(args, arg)))
    print("")
    if labeled:
        mat, label = load_features_and_labels(file_name)
        low_quality_cnt = len(label) - np.sum(label)
        print("total={}, low-quality={}, high-quality={}".format(len(label), low_quality_cnt, len(label) - low_quality_cnt))
    else:
        mat = load_features(file_name)
    feature_num = len(mat)
    cell_num = len(mat[0])
    print("{} features, {} cells".format(feature_num, cell_num))

    mat = min_max_scale(mat)
    tmat = np.array(list(zip(*mat)))
    similarity = cosine_similarity(tmat)

    start = time.time()
    sorted_feature_values = [np.sort(col) for col in mat]
    # Estimate range of low-quality cells
    if lower_bound is None and upper_bound is None:
        lower_bound = cell_num
        upper_bound = 0
        for col in sorted_feature_values:
            clf = IsolationForest(contamination='auto', random_state=0)
            values = np.array([[col[i]] for i in range(cell_num)])
            clf.fit(values)
            y_pred = clf.predict(values)
            num = np.sum(y_pred != 1)
            if num > cell_num / 2:
                continue
            lower_bound = min(lower_bound, num)
            upper_bound = max(upper_bound, num)
    print('range=[{},{}]'.format(lower_bound, upper_bound))

    # Get thresholds candidate list
    step = int((upper_bound - lower_bound + 1) * 0.2)
    threshold_candidate_lists = [col[lower_bound - 1: upper_bound: step] for col in sorted_feature_values]

    enumeration_list = list(itertools.product(*threshold_candidate_lists))
    total_rounds = len(enumeration_list)
    print(f"Total enumeration rounds: {total_rounds}")

    # Limit the number of enumeration rounds to 5
    enumeration_list = enumeration_list[:10]

    def progress_wrapper(args):
        result = run_enumeration_round_wrapper(args)
        progress_wrapper.counter += 1
        print(f"Completed {progress_wrapper.counter}/{len(enumeration_list)} rounds")
        return result

    progress_wrapper.counter = 0
    scores = Parallel(n_jobs=-1)(delayed(progress_wrapper)((thresholds, tmat, feature_num, cell_num, similarity)) for thresholds in enumeration_list)
    max_score_id = scores.index(max(scores))
    best_thresholds = enumeration_list[max_score_id]
    result = []
    run_single_enumeration_round(best_thresholds, tmat, feature_num, cell_num, similarity, result)
    if labeled:
        precision, recall, F1 = calc_pre_recall_F1(result, label)
        print('precision {:2f} recall {:2f} F1Score {:2f}'.format(precision, recall, F1))

    # Store the result to the output path
    if result_path:
        with open(result_path, 'w') as f:
            f.write('Quality\n')
            f.writelines('\n'.join(map(str, result)))
    end = time.time()
    print('Done. Total time: {:2f}s. Results have been stored in {}'.format(end - start, result_path))