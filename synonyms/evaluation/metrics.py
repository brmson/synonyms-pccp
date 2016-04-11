import math


def r_precision(synonym, sequence):
    size = len(sequence)
    return min(1, sum([1 for item in sequence if item in synonym[:size]]) / size)


def ndcg(relevance_sequence, k):
    max_dcg = dcg(sorted(relevance_sequence[:k], reverse=True), k)
    if max_dcg == 0:
        max_dcg = 1
    ndcg = dcg(relevance_sequence, k) / max_dcg
    return ndcg


def dcg(relevance_sequence, k):
    dcg = 0
    for i in range(k):
        dcg += (math.pow(2, relevance_sequence[i]) - 1) / math.log(i + 2, 2)
    return dcg