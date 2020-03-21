import Vue from 'vue'

var globalSearch = new Vue({
    el: '#global-search',
    data: {
        keyword: ''
    },
    methods: {
        onSearch: function () {
            if (globalSearch.keyword.length === 0) {
                location.href = '/';
                return;
            }
            location.href = '/?keyword=' + encodeURI(globalSearch.keyword);
        }
    }
});


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


var seqInputGroup = new Vue({
        el: '#input-seq-group',
        data: {
            seq: '',
            waitingBackend: false,
            validAmino: new Set('ARNDCEQGHVILKMFPSTWY')
        },

        methods: {
            _changeWaitingState: function(isWating) {
                seqInputGroup.waitingBackend = isWating;
            },
            findLrr: function () {
                if (seqInputGroup.seq.length === 0) {
                    alert("No sequence input");
                }
                seqInputGroup.seq = seqInputGroup.seq.replace(new RegExp('\\s', 'g'), '');
                for (let i = 0; i < seqInputGroup.seq.length; ++i) {
                    if (!seqInputGroup.validAmino.has(seqInputGroup.seq[i])) {
                        alert("Unexpected amino " + seqInputGroup.seq[i] + " at position " + i);
                        return;
                    }
                }

                seqInputGroup._changeWaitingState(true);
                $.ajax({
                    url: '/find-lrr',
                    method: 'POST',
                    contentType: "application/json",
                    data: JSON.stringify({seq: seqInputGroup.seq}),
                    success: function (response) {
                        seqInputGroup._changeWaitingState(false);
                        let seq = {
                            "seq": seqInputGroup.seq,
                            "motifs_16": response['LRRs']
                        };
                        colorSeqView.onSelectSeq(seq);
                    },
                    error: function (xhr, textStatus, errorThrown) {
                        seqInputGroup._changeWaitingState(false);
                        if (xhr.status === 429) {
                            $('#tooManyRequestAlert').modal('show');
                            return;
                        }
                        let errorBody = JSON.parse(xhr.responseText);
                        alert(errorThrown + ': ' + errorBody['message']);
                    }
                })
            }
        }
    });