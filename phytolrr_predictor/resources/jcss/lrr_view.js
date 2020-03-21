
var colorSeqView = new Vue({
    el: '#color-seq',
    data: {
        seq_id: '',
        sid: null,
        seqTexts: [],
        selectedIdToMotifs:{},
        motifTable: [],
        selectedSeq: {seq: ''}
    },
    filters: {
        fixFloat: function (value) {
            value = Number(value);
            return value.toFixed(3);
        }
    },
    methods: {
        _updateMotifTable: function(row) {
            let motif = colorSeqView.motifTable[row];
            Vue.set(colorSeqView.motifTable, row, motif);
        },
        _fullUpdateMotifTable: function(seqInput) {
            colorSeqView.motifTable = [];

            let motifs = seqInput['motifs_16'];

            for (let i = 0; i < motifs.length; i++) {
                let offset = motifs[i]['offset'];

                let motifStr = '';
                if (i < motifs.length - 1) {
                    motifStr = seqInput['seq'].slice(offset, motifs[i+1]['offset']);
                }
                else {
                    motifStr = seqInput['seq'].slice(offset);
                }

                let motifRow = {
                    row: i,
                    seq: motifStr,
                    offset: offset,
                    score: motifs[i]['score']
                };
                Vue.set(colorSeqView.motifTable, i, motifRow);
            }
        },
        _updateSeqText: function(seqInput) {
            colorSeqView.seqTexts = [];

            let nextOffset = 0;
            let seqIndex = 0;
            let motifs = seqInput['motifs_16'];
            let colorPoses = new Set();
            for (let i = 0; i < motifs.length; ++i) {
                let motif = motifs[i];
                if (motif.false_discovery) {
                    continue;
                }
                for (let pos = motif.offset; pos < motif.offset + 16; ++pos) {
                    colorPoses.add(pos);
                }
            }
            let plainSeq = seqInput.seq;
            for (let i = 0; i < plainSeq.length; ++i) {
                let seqText = {
                    offset: i,
                    seq: plainSeq[i],
                    highlight: false
                };
                if (colorPoses.has(i)) {
                    seqText.highlight = true;
                }
                Vue.set(colorSeqView.seqTexts, i, seqText);
            }
        },
        onSelectSeq: function (seqInput) {
            colorSeqView.selectedSeq = seqInput;
            colorSeqView._fullUpdateMotifTable(seqInput);
            colorSeqView._updateSeqText(seqInput);
        }
    }
});