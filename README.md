# MP1: Finite-state language modeling

## Finite-state morphophonology

The file `finnish_train.tsv` (in this repository) contains data on Finnish declension (i.e., nominal inflection) extracted from [Wiktionary](https://www.wiktionary.org/). The data consists of a 150-line TSV (tab-separated values) file in the following format:

    LEMMA	WORDFORM	MORPHOLOGY

where

* `LEMMA`: citation form (in orthography)
* `WORDFORM`: inflected word (in orthography)
* `MORPHOLOGY`: the wordform's morphology

All the data consist of singular nouns in the adessive ("near", "adjacent to") case, indicated by "AT+ESS" in `MORPHOLOGY`, or the inessive ("in", "inside") case, indicated by "IN+ESS" in `MORPHOLOGY`. These cases are marked by suffixes which show several allomorphs (i.e., contextual variants) due to a phenomenon known as _vowel harmony_. According to Ringen and Heinämäki (1999), which is included in this repository for your reference, the adessive suffix is usually realized as _-llä_ [lːæː] except when the preceding stem contains one of _u_, _o_, and _a_ and there is no intervening _y_, _ö_, or _ä_; in this case, it is _-lla_ [lːɑː]. For example, _käde_ 'hand’ has an adessive _kädellä_, whereas _vero_ ‘tax’ forms the adessive _verolla_ because the nearest stem vowel is) _o_. Similar rules hold for the inessive suffix, which has _-ssä_ [sːæː] and _-ssa_ [sːɑː] allomorphs. However, there are several other phonological factors at play in the provided data.

### What to do

Your assignment is to compile two sets of finite-state rules&mdash;one for the adessive, one for the inessive&mdash;which generate the wordforms from the corresponding lemma. Your solution needs to be sufficiently general that it is capable of generating the appropriate adessive and inessive forms for held-out examples. Your script should compile the rules and write them into a FAR file, as follows:

    with pynini.Far("finnish.far", "w") as sink:
        sink["ADESSIVE"] = your_adessive_rule
        sink["INESSIVE"] = your_inessive_rule

## What to turn in

* A script that generates `finnish.far` as described above, and
* A brief (roughly one-page) write-up describing the rules you posited, and providing:
    - the percentage of adessive examples in `finnish_train.tsv` covered by your rules
    - the percentage of inessive examples in `finnish_train.tsv` covered by your rules, and
    - some examples not covered by your rules and why they are not covered.

## Grading

You will be graded on:

* Your rules' coverage of the data in `finnish_train.tsv`,
* Your rules' coverage of a set of 50 held-out examples, and
* the quality and detail of your write-up.

## Hints

* Suffixation is just concatenation (`concat` or the `+` operator).
* Vowel harmony (and other changes) are best accomplished using `cdrewrite`.

## Test support

Use `finnish_train.tsv` to evaluate your solution as described above.

## T9

T9 ("Text on 9 keys"; Grover et al. 1998) is a patented predictive text entry method in which each of the 10 digit keys of a traditional 3x4 touch-tone phone grid maps onto a larger alphabet including alphabetic and punctuation characters. This transduction is massively ambiguous: for instance, `4604663` can be read as `go home` or `go hood`, among many other possibilities. Therefore, T9 makes use of a hybrid lexicon/language model to disambiguate.

## What to do

Your assignment is to build a simple version of a T9 decoder which maps input digit strings onto the alphabet consisting of digits, lowercase ASCII characters, the space character, and ASCII punctuation characters, using a language model to disambiguate.

First, construct an unweighted FST which supports the following mappings (simplified slightly from the original T9 spec):

    0: 0, <SPACE>
    1: 1, ASCII punctuation characters (`string.punctuation`)
    2: 2, a, b, c
    3: 3, d, e, f
    4: 4, g, h, i
    5: 5, j, k, l
    6: 6, m, n, o
    7: 7, p, q, r, s
    8: 8, t, u, v
    9: 9, w, x, y, z

Then, construct a trigram (or higher-order) language model over the output alphabet using the [OpenGrm-NGram](http://ngram.opengrm.org) tools. Then, create a decoder function which applies the input digit string to the mapping FST, scores the resulting lattice with the language model, and returns the shortest path string.

## What to turn in

* A working decoder script or function and any assets I will need to test it locally, and
* a brief (roughly one page) write-up describing any challenges that arose.

## Grading

You will be graded on:

* Your decoder's performance on a held-out data set,
* the quality of your decoder code, and
* the quality and detail of your write-up.

## Test support

Test your decoder by passing it sensible English strings in T9; it may get some wrong, but in general it should be able to recover your intended text.

## Hints

* Use `string_map` or `string_file` for constructing the mapper; don't forget to compute the `closure` so that your mapper can handle strings of arbitrary length; you will have to escape the square brackets, however.
* You can use the data from [MP0](https://gist.github.com/kylebgorman/3e28fc834962017c9ac01f7434485519) for your language model; however, you shouldn't tokenize the data for this task.
* When building the language model, take special care when handling the space character.

## Stretch goals

(These are entirely optional and should only be attempted after completing the rest of the assignment.)

* Create a test corpus and code to evaluate the label error rate of your decoder.
* Then, try different language model orders and compute the performance. Or, build a bigram or trigram language model over *word* tokens, and then map these words tokens onto character sequences.
