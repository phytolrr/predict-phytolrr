# An overview to the predict-phytolrr program

The `predict-phytolrr` program could identify LRRs effectively, especially for **LRR motifs in plant LRR-RLKs**.

The program is based on the position specific scoring matrix (PSSM) algorithm and its training dataset are 4000 LRR motifs highly conserved sequences (HCSs) from LRR-RLKs of 17 land plant species. Please find detailed information at [https://www.phytolrr.com/about](https://www.phytolrr.com/about).

# Install the program

`predict-phytolrr` can be installed using `pip` **ONLY** under Python3 environment:

```bash
$ pip install predict-phytolrr
``` 

A virtual environment(virtutalenv e.g.) is recommended to prevent the damage of the system-wide Python environment.

# Run the program

You can run the program in two ways:

* run predict-phytolrr from the command line
* import the phytolrr_predictor module in the python source code

## Predict Plant LRRs from the command line

The `predict-phytolrr` could accept sequence(s) in either directly input from the command line or in fasta file(s), predict the LRRs, and print out the results either in the command line or in html files.

### Two ways to feed the sequences

**First way:** The sequence can be written directly through the *command line*:
```bash
$ predict-phytolrr MKLPHLLPFLTLILFAFAFSMTLPLMSESHLSLLNNRTDQQ....(very long)
Prediction result for seq Unknown_from_cmd_line:
LRR offset 8, FLTLILFAFAFSMTLP, score 5.68619738546084
LRR offset 81, VTYLNLTHTGLQGTLT, score 17.662632191299593
LRR offset 105, LRVLALRNNSLQGSIP, score 36.37469484306763
LRR offset 129, LQVLRVSQNQLEGKIP, score 35.079609050990754
LRR offset 153, LQRLILSYNRLEGSIP, score 39.13663517011341
... many other results followed
```

**Second way:** The sequences can also be read from fasta files. Assuming the file `test.fasta` contains one or more sequences, to predict LRRs for all the sequences in the file, use the `-f` option to specify a fasta file:

```bash
$ predict-phytolrr -f test.fasta
The sequence AL3G49070.t1 contains unexpected amino *, will not be predicted
The sequence AL3G41990.t1 contains unexpected amino *, will not be predicted
The sequence AL8G14250.t1 contains unexpected amino *, will not be predicted
Prediction result for seq AL5G26370.t1:
LRR offset 82, VTGVDLGGLKLTGVVS, score 20.609043937370146
LRR offset 106, LRSLNLADNFFRGAIP, score 33.523950081875626
LRR offset 130, LQYLNMSNNFLGGVIP, score 34.2935452040218
LRR offset 154, LSTLDLSSNHLEQGVP, score 29.383744295363456
LRR offset 178, LVILSLGRNNLTGKFP, score 34.567366699698404
... other predicted LRRs for seq AL5G26370.t1

Prediction result for seq AL5G26330.t1:
LRR offset 74, VTRLDLGGLQLGGVIS, score 24.76974498840441
LRR offset 98, LISLNLYDNSFGGTIP, score 34.4857875432728
LRR offset 122, LQHLNMSYNFLGGGIP, score 31.754313744552327
LRR offset 146, LLELDLISNHLGHCVP, score 10.059227438374975

... many other results followed
```

More than one fasta files could also be accepted by using the `-f` option for each fasta file:

```bash
$ predict-phytolrr -f test1.fasta -f test2.fasta

... all prediction results for all sequences in test1.fasta and test2.fasta
```

### NOTE

1. Sequences with undefined amino acids, for instance "X", "*", will be skipped in the prediction process.
2. The asterisk "*" at the end of the fasta sequence will be removed automatically during the prediction process.

### To display the results in html

The result can also be dumped to HTML files, so that they can be viewed in a browser. Using the `-o` option to specify the root path of the resulting HTML files:

```bash
$ predict-phytolrr -f test1.fasta -o ./

... all prediction results for all leagal sequences in test1.fasta would be dumped to HTML files under the path `./`
```

## Predict Phyto LRRs in source code

TODO