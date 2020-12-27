from Bio.Seq import Seq
from Bio import motifs
from Bio.Alphabet import IUPAC


# The operation of the motif.pssm in Bio-python is very slow,
# storing pssm in dict/list could increase performance by more than 10,000 times.
class Matrix(object):
    def __init__(self, matrix):
        self.length = matrix.length
        self.pssm = {}
        for a in matrix.pssm:
            self.pssm[a] = [matrix.pssm[a][i] for i in range(0, self.length)]


def calc_pssm_matrix(motif_seqs_str, origin=False):
    """Generate the PSSM matrix from base line motifs `motif_seqs_str`"""
    motif_seq = [Seq(motif_seq_str, IUPAC.protein) for motif_seq_str in motif_seqs_str]
    matrix = motifs.create(motif_seq, IUPAC.protein)

    # Laplace smoothing(add pseudo-count)
    for p in matrix.pseudocounts:
        matrix.pseudocounts[p] = 1

    if origin:
        return matrix
    else:
        return Matrix(matrix)
