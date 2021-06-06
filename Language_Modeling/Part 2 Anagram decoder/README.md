# HW7: Anagram decoding, part 2

This is the second of a two-part assignment in which you will build a system to
decode "anagrammed" or "scrambled" English text, text in which each word's
characters have been randomly scrambled. For instance, given the "ciphertext"

    ot tsgusge htta eth peedrtnsi nwte sfto no ihtew sacpsimtuesr sutj to sesm wiht hte imdae is ot easusm htat he sode 'nt laeryl syamipzhte htiw trhie ircsat lbsfiee .

you will attempt to recover the "plaintext"

    to suggest that the president went soft on white supremacists just to mess with the media is to assume that he does n't really sympathize with their racist beliefs .

-   In part 1 of this assignment, **completed last week**, you built a language
    model over plaintext tokens.
-   In part 2 of this assignment, you will write and evaluate a "decoder" script
    using the language model built in part 1.

# Part 2: the decoder

Write the main method and argument parsing for a Python script
[`decode.py`](decode.py) which decodes a file of anagrammed sentences.

## Design

Conceptually, you will, for each sentence, construct an FSA lattice of possible
ways to decode the scrambled words into English words, then pick the
unscrambling which has the highest probability according to the language model.

More concretely, you will, for each scrambled word, add to the lattice an arc
representing each English words in-vocabulary (i.e., known to the language
model) it could be unscrambled as. Then, you will compose the lattice with the
language model, creating a weighted FSA in which each path is associated with a
language model probability. Then you will compute the shortest path and extract
the string it corresponds to.

### Finding candidates

How should one determine what in-vocabulary words a scrambled word might be
decoded as? While there are many possibilities, one simple and efficient
technique is as follows. Let us say that a (scrambled or unscrambled) word's
*key* is simply that word's characters sorted lexicographically. For instance,
the key of `following` `fgillnoow`.

```python
def get_key(s: str) -> str:
    """Computes the "key" for a given string."""
    return "".join(sorted(s))
```

Crucially, both a word and all of the ways it might be scrambled share a key.
Therefore, we can build a table that maps each key to real words. This is shown
in the following snippet; note that we use the integer index for an
in-vocabulary token rather than its string format.

```python
KeyTable = DefaultDict[str, List[int]]


def make_key_table(sym: pynini.SymbolTable) -> KeyTable:
    """Creates the key table.

    The key table is a dictionary mapping keys to the index of words which
    have that key.
    """
    table: KeyTable = collections.defaultdict(list)
    for (index, token) in sym:
        key = get_key(token)
        table[key].append(index)
    return table
```

### Building the lattice

Given a scrambled sentence, expressed as a list of scrambled strings, we can
then use the key table to build the lattice. This is a little hairy.

```python
def make_lattice(tokens: List[str], key_table: KeyTable) -> pynini.Fst:
    """Creates a lattice from a list of tokens.

    The lattice is an unweighted FSA.
    """
    lattice = pynini.Fst()
    # A "string FSA" needs n + 1 states.
    lattice.add_states(len(tokens) + 1)
    lattice.set_start(0)
    lattice.set_final(len(tokens))
    for (src, token) in enumerate(tokens):
        key = get_key(token)
        # Each element in `indices` is the index of an in-vocabulary word that
        # represents a possible unscrambling of `token`.
        indices = key_table[key]
        assert indices, f"no in-vocabulary items found for {token}"
        for index in indices:
            # This adds an unweighted arc labeled `index` from the current
            # state `src` to the next state `src + 1`.
            lattice.add_arc(src, pynini.Arc(index, index, 0, src + 1))
    assert lattice.verify(), "ill-formed lattice"
    return lattice
```

For instance, if the _i_-th scrambled token is `tni`, then there will be arcs
from state *i* to state *i* + 1 with labels corresponding to the words `nit`,
`tin`, etc. For the ciphertext

    si tihs ti ?

the lattice might resemble

![](img/lattice-no-symbols.png)

where 49 maps to `is`, 184 maps to `this`, and 48 maps to `it`, etc. (Lattices
of this shape are sometimes known as "sausages".)

### Scoring and decoding

The final steps of the decoding process are straightforward.

1.  We compose the lattice produced by `make_lattice` with the LM, optionally
    checking to make sure composition was successful.
2.  We compute the shortest path through the lattice.
3.  We convert this into a tokenized string.

The following function takes care of these steps:

```python
def decode_lattice(
    lattice: pynini.Fst, lm: pynini.Fst, sym: pynini.SymbolTable
) -> str:
    """Scores and decodes the lattice."""
    lattice = pynini.compose(lattice, lm)
    assert lattice.start() != pynini.NO_STATE_ID, "composition failure"
    # Pynini joins the string for us.
    return pynini.shortestpath(lattice).string(sym)
```

### Program structure

The `main` should flow as follows.

1.  Load the n-gram language model from part 1 using `pynini.Fst.read`, which
    takes a input file path as an argument.

2.  Extract the symbol table from the language model FST using the FST's
    `input_symbols()` method.

    ```python
    sym = lm.input_symbols()
    assert sym, "no input symbol table found"
    ```

3.  Use `make_key_table` and the symbol table extracted in the previous step to
    generate the key table.

4.  Open the scrambled input file for reading and the output file for writing.

5.  For each line/sentence of the input file:
    1.  Split the sentence on whitespace using
        [`str.split`](https://docs.python.org/3.3/library/stdtypes.html?highlight=split#str.split)
        to create a list of tokens.
    2.  Construct the lattice using `make_lattice` and the key table generated
        in the previous step.
    3.  Compose the lattice with the LM loaded in the first step.
    4.  Compute the shortest path string using `decode_lattice` and write it to
        the output file.

A suggested command-line invocation of `decode.py` might look like the
following:

```bash
./decode.py --lm=en.lm data/test.ana data/test.hyp
```

## What to turn in

1.  An executable Python program [`decode.py`](decode.py).
2.  A file named `data/test.hyp` containing the output from running that program
    on the anagrammed text in [`data/test.ana`](data/test.ana).
3.  A one-page write-up, in PDF form, detailing any challenges you experienced
    and how you dealt with them.

Once again, *do not* upload any files created by the NGram tools to GitHub. They
can be quite large and I don't need them.

## Hints

-   The included [`decode.py`](decode.py) contains the snippets above; you just
    have to add a `main`, and a main-guard with argument parsing below this
    code.
-   Read the [`defaultdict`
    documentation](https://docs.python.org/3.3/library/collections.html#collections.defaultdict).
-   When decoding, do not read the entire file at once. Instead, decode one line
    at a time, printing out the result one sentence at a time.
-   Note that the key table only needs to be constructed once, not once per
    sentence.
-   Inspect the decoder output (e.g., the file `data/test.ana`). It should look
    English-like, modulo tokenization, case-folding, and the occasional decoding
    error.

## Stretch goal

Write a Python script `evaluate.py` which computes the word and sentence
accuracy of your decoder. This should take two arguments: a "gold" file
containing unscrambled text, and a "hypothesis" file of the same length, and
print out two accuracy statistics as percentages.

-   *Word accuracy* is simply the percentage of correctly unscrambled tokens.
-   *Sentence accuracy* is the percentage of sentences for which all tokens are
    correctly unscrambled.

Multiply both of these accuracies by 100 and express as an integer percentage
(e.g., "95%"). (This is going to be an integer because there are only 100
sentences in the dev and test files.)

Apply [`decode.py`](decode.py) to the included [`data/dev.ana`](data/dev.ana)
file, then use this and the gold file [`data/dev.tok`](data/dev.tok) to compute
word and sentence accuracy.
