from argparse import ArgumentParser
import phytolrr_predictor
from phytolrr_predictor.tools.exception import ValidationError
import sys
import os
import logging
from typing import List
from Bio import SeqIO


class Sequence:
    def __init__(self, seq_id, seq):
        self.id = seq_id
        self.seq = seq


class PredictResult:
    def __init__(self, seq:Sequence, ret:List[phytolrr_predictor.motifs.Motif]):
        self.seq = seq
        self.ret = ret


def is_seq_valid(seq_id, seq):
    VALID_AMINO = {'A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'V', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y'}
    for amino in seq:
        if amino not in VALID_AMINO:
            logging.warning("The sequence {} contains unexpected amino {}, will not be predicted".format(seq_id, amino))
            return False
    return True


def read_seqs_from_files(file_paths:List[str]) -> List[Sequence]:
    seqs = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise ValidationError(1, "The file %s does not exists".format(file_path))
        if not os.path.isfile(file_path):
            raise ValidationError(1, "The path %s is not a file".format(file_path))
        for record in SeqIO.parse(file_path, "fasta"):
            seq = Sequence(record.id, record.seq.__str__())
            if seq.seq.endswith('*'):
                seq.seq = seq.seq[:-1]
            if not is_seq_valid(seq.id, seq.seq):
                continue
            seqs.append(seq)
    return seqs


def build_seq_from_str(seq_str:str) -> Sequence:
    if not is_seq_valid("inputted", seq_str):
        return None
    return Sequence("Unknown_from_cmd_line", seq_str)


def predict_seqs(seqs:List[Sequence]) -> List[PredictResult]:
    rets = []
    for seq in seqs:
        ret = phytolrr_predictor.predict(seq.seq)
        if ret is None:
            raise Exception("Unexpected error, None result when predicting " + seq.id)
        rets.append(PredictResult(seq, ret))
    return rets


def print_result(rets:List[PredictResult]):
    first = True
    for ret in rets:
        if not first:
            logging.info('')
        first = False
        ret.ret.sort(key=lambda m:m.offset)
        logging.info("Prediction result for seq {}:".format(ret.seq.id))
        for m in ret.ret:
            logging.info(str.format("LRR offset {}, {}, score {}", m.offset, ret.seq.seq[m.offset:m.offset+16], m.score))


def dump_html(path:str, ret:List[PredictResult]):
    raise ValidationError(1, "Does not support dump to html files yet")


def main():
    parser = ArgumentParser(description='Predict LRRs(Leucine-Rich Repeat) from sequences')
    parser.add_argument('sequence', nargs='?', help='The sequence wish to be predicted.')
    parser.add_argument('-f', '--files', action='append',
                        help='Path(s) to the file containing sequences to be predicted. '
                             'The file(s) must be in FASTA format.')
    parser.add_argument('-p', '--output-prefix',
                        help='The directory path to save result file(s) in HTML format. '
                             'If the option does not exists, the result will be printed on the screen.')

    args = parser.parse_args()
    if args.sequence is None and args.files is None:
        raise ValidationError(1, "At least one sequence string or sequence file "
                                 "should be specified for prediction.")

    seqs = []
    if args.files is not None:
        seqs = read_seqs_from_files(args.files)
        if len(seqs) == 0:
            raise ValidationError(1, "No valid sequences found in files {}".format(args.files))

    if args.sequence is not None:
        seq = build_seq_from_str(args.sequence)
        if seq is None:
            raise ValidationError(1, "The sequence input is invalid, and the prediction process will exit")
        seqs.append(seq)

    rets = predict_seqs(seqs)
    if args.output_prefix is None:
        print_result(rets)
    else:
        dump_html(args.output_prefix, rets)

    return 0


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        exit(main())
    except ValidationError as e:
        if e.message == 1:
            logging.error("Error: " + e.detail)
            logging.error("Please enter `{} -h` to see the usage.".format(sys.argv[0]))