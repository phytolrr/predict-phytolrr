from argparse import ArgumentParser
import phytolrr_predictor
from phytolrr_predictor.tools.exception import ValidationError
from phytolrr_predictor.tools import pssm_matrix
from phytolrr_predictor.tools import motifs as motifs_tools
import sys
import os
import json
import shutil
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
            print("Warning: The sequence {} contains unexpected amino {}, will not be predicted".format(seq_id, amino))
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
    if seq_str.endswith('*'):
        seq_str = seq_str[:-1]
    if not is_seq_valid("inputted", seq_str):
        raise ValidationError(1, "The sequence input is invalid, and the prediction process will exit")
    return Sequence("Unknown_from_cmd_line", seq_str)


def predict_seqs(seqs:List[Sequence], training_dataset=None) -> List[PredictResult]:
    if training_dataset is None:
        matrix = None
    else:
        matrix = pssm_matrix.calc_pssm_matrix(training_dataset)
    rets = []
    for seq in seqs:
        ret = phytolrr_predictor.predict(seq.seq, matrix)
        if ret is None:
            raise Exception("Unexpected error, None result when predicting " + seq.id)
        rets.append(PredictResult(seq, ret))
    return rets


def print_result(rets:List[PredictResult], length=16):
    first = True
    for ret in rets:
        if not first:
            print('')
        first = False
        ret.ret.sort(key=lambda m:m.offset)
        print("Prediction result for seq {}:".format(ret.seq.id))
        for m in ret.ret:
            print(str.format("LRR offset {}, {}, score {}", m.offset, ret.seq.seq[m.offset:m.offset+length], m.score))


def dump_html(path:str, rets:List[PredictResult], length=16):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.isdir(path):
        raise ValidationError(1, "Error: the output path {} specified must be a directory".format(path))

    results = []
    for ret in rets:
        results.append({
            'seq_id': ret.seq.id,
            'seq': ret.seq.seq,
            'motifs_16': [{'offset': m.offset, 'score': m.score, 'length': length} for m in ret.ret]
        })
    with open(os.path.join(path, 'results.js'), 'w') as f:
        f.write('let results = ')
        f.write(json.dumps(results))
        f.write(';')

    module_path = os.path.join(os.path.dirname(__file__), 'phytolrr_predictor', 'resources')
    html_file_path = os.path.join(module_path, 'results.html')
    shutil.copyfile(html_file_path, os.path.join(path, 'results.html'))

    print("{} sequences were predicted and the results have been saved in the file {}.".
          format(len(results), html_file_path))


def read_motifs_from_file(file_path):
    with open(file_path) as f:
        motifs = [m.strip() for m in f.readlines()]
    if len(motifs) == 0:
        print("empty file")
        exit(1)
    length = None
    for m in motifs:
        if length is None:
            length = len(m)
            if length == 0:
                print("Empty line exists")
                exit(1)
            continue
        if length != len(m):
            print("The length of all motifs should be the same.")
            exit(1)
    return motifs, length


def main_run():
    parser = ArgumentParser(description='Predict LRRs(Leucine-Rich Repeat) from sequences')
    parser.add_argument('sequence', nargs='?', help='The sequence wish to be predicted.')
    parser.add_argument('-f', '--files', action='append',
                        help='Path(s) to the file containing sequences to be predicted. '
                             'The file(s) must be in FASTA format.')
    parser.add_argument('-p', '--output-prefix',
                        help='The directory path to save result file(s) in HTML format. '
                             'If the option does not exists, the result will be printed on the screen.')
    parser.add_argument('-t', '--training-dataset',
                        help='Specify a path to a file which contains training LRR motifs '
                             'to replace the built-in motifs.')

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
        seqs.append(build_seq_from_str(args.sequence))

    length = 16
    if args.training_dataset is None:
        rets = predict_seqs(seqs)
    else:
        dataset, length = read_motifs_from_file(args.training_dataset)
        rets = predict_seqs(seqs, dataset)
    for seq_ret in rets:
        seq_ret.ret = motifs_tools.found_no_overlapped_motifs(seq_ret.ret, length)
    if args.output_prefix is None:
        print_result(rets, length)
    else:
        dump_html(args.output_prefix, rets, length)

    return 0


def main():
    try:
        return main_run()
    except ValidationError as e:
        if e.message == 1:
            print("Error: " + e.detail)
            print("Please enter `{} -h` to see the usage.".format(sys.argv[0]))


if __name__ == "__main__":
    main()
