# -*- coding: utf-8 -*
import math
import logging
import numpy


def calc_probability_by_score(score):
    return float(numpy.power(2, score * -1))


class Motif(object):
    def __init__(self, offset, seq_id, score):
        self.offset = offset
        self.seq_id = seq_id
        self.score = score
        self.probability = calc_probability_by_score(self.score)
        self.fdr_probability = None  # generated in fdr_procedure


def calc_pssm_score(seq, m):
    score = 0.0
    for i in range(0, len(seq)):
        letter = seq[i]
        score += m.pssm[letter][i]
        if math.isinf(score) and score < 0:
            break
    return score


def generate_motifs_with_pssm_score(seq, m):
    motifs = []
    count = 0
    for i in range(0, len(seq) - m.length + 1):
        sub_seq = seq[i:i + m.length]
        count += 1
        m_score = Motif(i, None, calc_pssm_score(sub_seq, m))
        motifs.append(m_score)
    return motifs


def _fdr_procedure(motifs):
    motifs.sort(key=lambda k: k.probability, reverse=True)
    for i, motif in enumerate(motifs):
        motif.fdr_probability = 0.05 * i / len(motifs)
    return [m for m in motifs if m.probability < m.fdr_probability]


def lrr_search(matrix, seq):
    # generate the PSSM score and probability
    logging.debug("Begin to generate the PSSM score and probability...")
    motifs_score = generate_motifs_with_pssm_score(seq, matrix)

    # FDR procedure
    logging.debug("Do the BH procedure(FDR)")
    return _fdr_procedure(motifs_score)


def get_highest_score_recursively(current_index, offsets, total_score, last_score, length, motifs):
    if current_index >= len(motifs):
        return total_score, offsets

    current_motif = motifs[current_index]

    if offsets[-1] + length <= current_motif.offset:
        offsets.append(current_motif.offset)
        return get_highest_score_recursively(current_index + 1, offsets,
                                             total_score + current_motif.score, current_motif.score,
                                             length, motifs)
    else:
        # 出现重叠，干掉自己或者干掉上一个看看那个score更高
        return max(
            # 干掉自己
            get_highest_score_recursively(current_index + 1, offsets[:],
                                          total_score, last_score,
                                          length, motifs),

            # 干掉上一个
            get_highest_score_recursively(current_index + 1, offsets[:-1] + [current_motif.offset],
                                          total_score - last_score + current_motif.score, current_motif.score,
                                          length, motifs),

            key=lambda x: x[0]
        )


def get_highest_score_without_overlay(motifs, length):
    ordered_motifs = list(motifs)
    ordered_motifs.sort(key=lambda m: m.offset)

    offsets = [ordered_motifs[0].offset]
    score = ordered_motifs[0].score
    score, no_overlap_offsets = get_highest_score_recursively(1, offsets, score, score, length, ordered_motifs)
    no_overlap_offsets = set(no_overlap_offsets)

    return score, [m for m in ordered_motifs if m.offset in no_overlap_offsets]


def found_no_overlapped_motifs(motifs, length=16):
    if len(motifs) == 0:
        return []
    score, motifs = get_highest_score_without_overlay(motifs, length)
    return motifs
