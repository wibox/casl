ANSWERS:
1) What are the inputs and outputs of the software?
The software takes as input a (hard-coded) list of lenghts to build token (default to 4 and 8) and a list of number of bits to use to store the fingerprint of each sentence and the path of the original text file on which work is done; it outputs informations regarding the original text file (number of unique words, verses and total number of words) as well as informations circa the processed text file (number of sentences built using tokens of lenght 4 and 8, total memory occupancy of stored sentences and corresponding fingerprints as well as False positive probabilities of conflicts w.r.t. fingerprints built on a given range function of the number of bits given as input). Eventually, plots of fingerprint's size and total memory occupancy are provided in function of Pr[FP].

2) The number of stored sentences is:
	length 4 -> 96382
	length 8 -> 96378
Sentences stored in the set are less that the actual computed number due to conflicts caused by preprocessing.

3) The original text file takes 543.2 Kb, 4grams take 2.0 Mb and 8grams 4.1 Mb.

4) Storing 4grams in a python set takes 11407.42 Kb, while storing 8grams in a python set takes 13813.09 Kb.

5) utils.FingerprintHandler class takes care of this.

6 & 7) Look in results/ for graph.
	The relation between fingerprint size (bits) and Pr[FP] is:
	Pr[FP] = 1 - (1 - 1/(2^(n_bits) - 1))^m

8) Memory occupancy is always improved when storing fingerprints instead of full 4/8grams in a python set. Such performance is independent for S due to the fact that when building a fingerprint the lenght of the string is not relevant for the hash function in terms of range.

