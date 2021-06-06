# HW6: Anagram decoding, part 1

This is the first of a two-part assignment in which you will build a system to
decode "anagrammed" or "scrambled" English text, text in which each word's
characters have been randomly scrambled. For instance, given the "ciphertext"

    ot tsgusge htta eth peedrtnsi nwte sfto no ihtew sacpsimtuesr sutj to sesm wiht hte imdae is ot easusm htat he sode 'nt laeryl syamipzhte htiw trhie ircsat lbsfiee .

you will attempt to recover the "plaintext"

    to suggest that the president went soft on white supremacists just to mess with the media is to assume that he does n't really sympathize with their racist beliefs .

-   In part 1 of this assignment you will build a language model over plaintext
    tokens.
-   In part 2 of this assignment, **which will be completed next week**, you
    will write and evaluate a "decoder" script that uses your language model.

# Part 1: language model construction

## What to do

Build a English trigram language model over tokens.

1.  Install the OpenGrm-NGram library and [`nltk`](https://www.nltk.org/):
    `conda install -c conda-forge ngram nltk`.
3.  Download the [2007 News Crawl
    data](http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2007.en.shuffled.gz)
    from [WMT \'14 translation
    task](http://www.statmt.org/wmt14/translation-task.html). You can do this in
    your web browser, with command-line tools like
    [`wget`](https://linux.die.net/man/1/wget) or
    [`curl`](https://linux.die.net/man/1/curl), or using Python libraries like 
    [`urllib.requests`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request)
    or the third-party [`requests`](https://docs.python-requests.org/en/master/).
    (The Python options are not for the faint of heart.)

3.  Prepare the text data. Write a Python script `prepare.py` which
    decompresses, tokenizes, and case-folds the data, then run the script over
    the 2007 News Crawl data downloaded in the previous step.

    1.  The file is compressed using gzip format and has to be decompressed
        during reading. Open it using
        [`gzip.GzipFile`](https://docs.python.org/3/library/gzip.html#gzip.GzipFile).
    2.  Each line of the decompressed News Crawl data is a single sentence.
        Iterating over the gzip file opened in the previous step, one
        sentence/line at a time,
        1.  apply
            [`nltk.tokenize.word_tokenize`](https://www.nltk.org/api/nltk.tokenize.html?highlight=nltk%20word_tokenize#nltk.tokenize.word_tokenize),
        2.  use the
            [`str.join`](https://docs.python.org/3/library/stdtypes.html#str.join)
            to create a string where each token in the sentence is separated by
            space,
        3.  use the
            [`str.casefold`](https://docs.python.org/3/library/stdtypes.html#str.casefold)
            to create a lowercase version of the tokenized sentence, and
        4.  write the tokenized, case-folded sentence string to a new file using
            [`print`](https://docs.python.org/3/library/functions.html#print).
    3.  The resulting file should contain one tokenized, case-folded sentence
        on each line.
    4.  Use good style here, including argument parsing and a main-guard.

4.  Using the data produced in the preceding step, create a trigram token
    language model with Kneser-Ney smoothing. Let us suppose that the data file
    produced in the preceding step is called `en.tok`. Then run the following
    at the command line:

    ```bash
    ngramsymbols en.tok en.sym
    farcompilestrings \
        --fst_type=compact \
        --symbols=en.sym \
        --keep_symbols \
        en.tok \
        en.far
    ngramcount --order=3 en.far en.cnt
    ngrammake --method=kneser_ney en.cnt en.lm
    ngraminfo en.lm  # Prints some summary information about the model.
    ```
## What to turn in

1.  An executable Python program `prepare.py`.
2.  The output from `ngraminfo`, as above.
3.  A one-page write-up, in PDF form, detailing any challenges you experienced
    and how you dealt with them.

**Do not** upload the files created by the NGram tools to GitHub. They can be
quite large and I don't need them.

## Hints

-   Remember to include the shebang and to use `chmod +x` to make `prepare.py`
    executable.
-   When decompressing the data, **do not** decompress and read the entire file
    at once. Rather, work one line at a time.
-   Note that the command-line parts may take several minutes to run. If you're
    unsure if you're doing things right, try it with a smaller file (e.g., the
    first 1000 sentences) first.
-   While you are building a "2nd-order" Markovian language model, specify
   `--order=3` when calling `ngramcount`, indicating a trigram model. This kind
    of terminological ambiguity/inclarity is not uncommon when using third-party
    tools.
-   One easy way to test your language model is to randomly sample "sentences"
    from it. This can be done from the command line as follows:

    ```bash
    ngramrandgen --max_sents=1 en.lm | farprintstrings
    ```
    
    Note that the output is at best, locally-coherent nonsense.
-   Read the [NGram quick
    tour](http://www.openfst.org/twiki/bin/view/GRM/NGramQuickTour) if you
    want more context.

## Stretch goal

Instead of running the n-gram model-building steps manually, from the command
line, write a Python script which runs these commands using
[`subprocess.check_call`](https://docs.python.org/3/library/subprocess.html#subprocess.check_call).
In addition to the paths, the script should take arguments such as model order
and smoothing method.
