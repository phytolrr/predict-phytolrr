
const seqsRow = new Vue({
    el: '#navigator-view',
    data: {
        total: results.length,
        activeSeq: null,
        seqs: [],
        keyword: "",
        pageIndex: 0,
        pageSize: 10,
        goToIndex: 0,
        waitingBackend: false,
        value: null
    },
    methods: {
        _selectSeq: function(seq) {
            colorSeqView.onSelectSeq(seq)
        },
        onSelect: function (seq) {
            seqsRow._selectSeq(seq);
        },
        changePage: function (page, size) {
            seqsRow.pageIndex = page;
            seqsRow.goToIndex = seqsRow.pageIndex + 1;
            seqsRow.pageSize = size;
            let start = seqsRow.pageIndex * seqsRow.pageSize;
            let end = start + seqsRow .pageSize;
            if (end > results.length) {
                end = results.length;
            }
            seqsRow.seqs = results.slice(start, end);
        },
        prevPage: function () {
            if (seqsRow.pageIndex > 0) {
                seqsRow.changePage(seqsRow.pageIndex - 1, seqsRow.pageSize);
            }
        },
        nextPage: function () {
            if (seqsRow.pageIndex < Math.ceil(seqsRow.total/seqsRow.pageSize) - 1) {
                seqsRow.changePage(seqsRow.pageIndex + 1, seqsRow.pageSize);
            }
        },
        goTo: function() {
            let index = seqsRow.goToIndex - 1;
            if (index >= 0 && index <= Math.ceil(seqsRow.total/seqsRow.pageSize) - 1) {
                seqsRow.changePage(index, seqsRow.pageSize);
            }
        },
        onChangePageSize: function () {
            seqsRow.changePage(seqsRow.pageIndex, seqsRow.pageSize);
        }
    }
});