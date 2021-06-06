# HW8: Homograph disambiguation

In this lab, we will experiment with multinomial linear classifiers using
[scikit-learn](https://scikit-learn.org/).

*Homographs* are polysemous words whose senses are associated with different
pronunciations. For instance, the English word *bass* has (at least) three
senses:

1.  a musical "part", as in *bass clef* or *bass voice*
2.  a string instrument, as in *bass guitar* or *double bass*
3.  the name given to various species of fish of the order *Perciformes*

Senses 1-2 are pronounced \['beɪs\] and sense 3 is pronounced \['bæs\].

In homograph disambiguation, we attempt to predict the appropriate
pronunciation, e.g., for speech recognition or synthesis. This problem has
historically been approached using hand-written rules, but such approaches are
brittle and difficult to debug. Gorman, Mazovetskiy, and Nikolaev (2018),
henceforth GMN, use regularized multinomial logistic regression (specifically,
one classifier for each homograph set) to predict the appropriate pronunciation.
We will attempt to recreate the GMN system using open-source tools.

We will use the same features, but separate classifiers, for each homograph.
Therefore, we will have to loop over homograph sets during training and
evaluate.

## Part 1: preparation

Install scikit-learn:

```bash
conda install sklearn
```

or

```bash
pip install sklearn
```

### What to turn in

Nothing for this section.

## Part 2: feature extraction

GMN release a free data set for homograph disambiguation, here stored in 
the [`data/`](data/) directory. It consists of sentences from English
Wikipedia in which 162 common homograph sets are labeled for their
pronunciation (from a fixed list of "lexicon" pronunciations). There
are roughly 90 training examples for each homograph set (in the `data/train`
subdirectory) and 10-11 test examples in the (`data/test` subdirectory). Most
homographs have 2 possible pronunciations, though a few have three.

Given a homograph in position *t*, extract the following features:

1.  case-folded token in *t* - 1, or `[NUMERIC]` if the token is numeric
2.  case-folded token in *t* - 2, or `[NUMERIC]` if the token is numeric
3.  case-folded token in *t* + 1, or `[NUMERIC]` if the token is numeric
4.  case-folded token in position *t* + 2, or `[NUMERIC]` if the token is
    numeric
5.  the concatenation of features (1, 2); i.e., the previous bigram
6.  the concatenation of features (3, 4); i.e., the following bigram
7.  the concatenation of features (1, 3); i.e., the skipgram bigram
8.  whether the homograph is uppercase, lowercase, titlecase, or none of the
    above

For instance, given the sentence *Bruno plays upright bass, guitar, a little
banjo, ukulele, and mandolin.*, in which the homograph *bass* is found in the
character range 20-24, one might produce the following features:

1.  `t-1`: `upright`
2.  `t-2`: `plays`
3.  `t+1`: `,`
4.  `t+2`: `guitar`
5.  `t-2^t-1`: `plays^upright`
6.  `t+1^t+2`: `,^guitar`
7.  `t-1^t+1`: `upright^,`
8.  `cap(t)`: `lower`

This is similar to GMN's "embedded" model.

Complete the implementation of the following feature extraction function, which
takes the sentence string, the homograph string, and start and end indices from
the GMN data files, and returns a dictionary of key-value pairs where the key is
the name of the feature and the value is the feature.

```python
from typing import Dict


FeatureVector = Dict[str, str]


def extract_features(
    sentence: str, homograph: str, start: int, end: int
) -> FeatureVector:
    Extracts  feature vector for a single sentence."""
    # There is some tricky stuff to find the target homograph word here.
    sentence_b = sentence.encode("utf8")
    left = sentence_b[:start]
    target = b"^" + sentence_b[start:end] + b"^"
    right = sentence_b[end:]
    sentence = (left + target + right).decode("utf8")
    tokens = nltk.word_tokenize(sentence)
    t = -1
    for (i, token) in enumerate(tokens):
        if token.count("^") == 2:
            t = i
            break
    assert t != -1, f"target homograph {homograph!r} not found"
    target = tokens[t].replace("_", "")
    # Now onto feature extraction.
    features: Dict[str, str] = {}
    # TODO: add features to the feature dictionary here using `token`, its
    # index `t`, and the list of tokens `tokens`.
    ...
    return features
```

### What to turn in

Nothing for this section.

### Hints

-   You will want to think of something clever to do in the case that the
    homograph word is the first, second, penultimate, or ultimate token.
-   Python strings have a method
    [`isnumeric`](https://docs.python.org/3/library/stdtypes.html#str.isnumeric)
    which can be used to determine where a token is numeric.
-   Python strings also have methods such as 
    -   [`casefold`](https://docs.python.org/3/library/stdtypes.html#str.casefold),
    -   [`islower`](https://docs.python.org/3/library/stdtypes.html#str.islower),
    -   [`isnumeric`](https://docs.python.org/3/library/stdtypes.html#str.isnumeric),
    -   [`istitle`](https://docs.python.org/3/library/stdtypes.html#str.istitle),
        and
    -   [`isupper`](https://docs.python.org/3/library/stdtypes.html#str.isupper),
    
    which can be used to extract the case feature.

## Part 3: training and prediction

Loop over each TSV file in `data/train`. For each file:

1.  Extract all the features and `wordid`s (the classes or labels).
2.  One-hot-encode the features using the
    [`DictVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html#sklearn-feature-extraction-dictvectorizer)'s
    `fit_transform` method.
3.  Fit a
    [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html#sklearn-feature-extraction-dictvectorizer)
    to predict `wordid` using its `fit` method.
4.  Extract all the features and `wordid`s from the corresponding TSV file in
    `data/test`. E.g., if the training TSV is `data/train/bass.tsv`, the test
    TSV is `data/test/bass.tsv`.
5.  One-hot-encode the test data features using the `transform` method of the
    `DictVectorizer` created in step 2.
6.  Predict the labels for the test data features using the `predict` method of
    the `LogisticRegression` you fit in step 3.
7.  Compute the number of correct and incorrect predictions by comparing the
    predictions generated in step 6 to the actual `wordid`s.

GMN al. compute *micro-averaged* and *macro-averaged* accuracy:

> The former is simply the percentage of examples correctly classified across
> all homographs; the latter is the arithmetic mean of the per-homograph
> accuracies. (p. 1351)

Using the correct and incorrect counts you computed in step 7, compute the
micro- and macro-averaged accuracy for your classifiers.

### What to turn in

1.  The code for a script [`train_eval.py`](train_eval.py) which performs the
    above operations. You should use a `main` and `main`-guard but you do not
    need to use `argparse`: the sample code is set up to automatically iterate
    over the training data using a hard-coded path.
2.  The micro- and macro-averaged accuracies you computed.
3.  A one-page write-up, in PDF form, detailing any challenges you experienced
    and how you dealt with them.

### Hints

-   Remove the TODOs and ellipses before turning in your code.
-   `data/wordids.tsv` contains the mapping between homograph, wordid, and
    pronunciation for this data, in case you're interested in what a `wordid`
    means.
-   The TSV files have a header row so you may want to use
    [`csv.DictReader`](https://docs.python.org/3/library/csv.html#csv.DictReader).
    I have not tested reading this data with
    [`pandas`](https://pandas.pydata.org/).
-   You have to convert the `start` and `end` indices from `str` to `int` before
    passing them to `extract_features`.
-   To stay [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), I used
    a function that repeatedly calls `extract_features`.

```python
from typing import List, Tuple


FeatureVectors = List[FeatureVector]


def extract_features_file(path: str) -> Tuple[FeatureVectors, List[str]]:
    """Extracts feature vectors for an entire TSV file."""
    features: List[Dict[str, str]] = []
    labels: List[str] = []
    with open(path, "r") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            labels.append(row["wordid"])
            features.append(
                extract_features(
                    row["sentence"],
                    row["homograph"],
                    int(row["start"]),
                    int(row["end"]),
                )
            )
    return features, labels
```

-   Before you begin, read the user guide and documentation for `DictVectorizer`
    ([user
    guide](https://scikit-learn.org/stable/modules/feature_extraction.html#dict-feature-extraction),
    [docs](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html#sklearn-feature-extraction-dictvectorizer))
    and `LogisticRegression` ([user
    guide](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression),
    [docs](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression)).
-   Make sure you understand the difference between `DictVectorizer`'s `fit` and
    `fit_transform` methods.
-   Suggested (non-default) parameters for `LogisticRegression`:
    `penalty="l1"`,`C=10`,`solver="liblinear"`. With this setup, I saw one
    `ConvergenceWarning`; don't worry about it.
-   For the evaluation, I constructed two lists of integers: `correct`, which
    contains the number of correctly-classified homographs for each homograph
    set, and `size`, which contains the number of examples. Then,
    -   micro-averaged accuracy is computed by summing those up (one is the
        numerator, one the denominator), and
    -   macro-averaged accuracy is computed by computing, for each homograph,
        the accuracy, and then computing the mean of these accuracies. Python's
        built-in
        [`statistics`](https://docs.python.org/3/library/statistics.html#statistics.mean)
        library has a
        [`mean`](https://docs.python.org/3/library/statistics.html#statistics.mean)
        function, which might help with the latter step.
-   scikit-learn has a [`metrics`
    module](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics),
    but I supect figuring out how to use it here is harder than just computing
    the statistics yourself.
-   Similarly, scikit-learn's
    [pipelines](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
    are probably more trouble than they're worth here.

## Stretch goals

-   During feature extraction, POS-tag each sentence (e.g., using one of the
    [NLTK POS taggers](https://www.nltk.org/api/nltk.tag.html)) and use the tag
    assigned to the target word as an additional feature. Does this help or hurt
    performance?
-   Add some other new feature and repeat the evaluation. Does this help or hurt
    performance?
-   Use [Wilson score
    intervals](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval)
    to compute 95% confidence intervals for micro-accuracy.

## References

K. Gorman, G. Mazovetskiy, and V. Nikolaev. 2018. Improving homograph
disambiguation with machine learning. In *Proceedings of the Eleventh
International Conference on Language Resources and Evaluation*, pages 1349-1352.
