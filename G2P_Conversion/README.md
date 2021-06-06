# HW4: Rule-based G2P

*Grapheme-to-phoneme conversion* (g2p) is the task of converting words
(expressed orthographically, as grapheme sequences) to their phonemic
transcriptions. This task is an important part of speech technologies, including
recognition and synthesis.

## Goal

In this assignment, you will use [Pynini](http://pynini.opengrm.org/) to write a
series of grapheme-to-phoneme conversion rules for the Porto Alegre dialect of
Portuguese, as described by Beesley & Karttunen (2003:146f.).

Here are the major rules:

1.  *ch* is pronounced /ʃ/ (e.g., *chato* /ʃatu/ 'flat')
2.  *lh* is pronounced /ʎ/ (e.g., *vermelho* /veɾmeʎu/ 'red')
3.  *nh* is pronounced /ɲ/ (e.g., *gatinho* /gatʃiɲu/ 'kitten')
4.  Elsewhere *h* is silent (e.g., *homem* /omem/ 'male')
5.  *e* is pronounced /i/ finally and before final /s/ (e.g., *case* /kazi/ 'I
    would marry', *cases* /kazis/ 'you would marry')
6.  *o* is pronounced /u/ finally and before final /s/ (e.g., *braço* /brasu/
    'arm', *braços* /brasus/ 'arms')
7.  *c* before /i, e/ is pronounced /s/ (e.g., *cimento* /simentu/ 'cement')
8.  *c* is pronounced as /k/ elsewhere (e.g., *casa* /kaza/ 'house')
9.  *ç* is pronounced /s/ (e.g., *taça* /tasa/ 'cup')
10. *s* is pronounced /z/ intervocalically (i.e., between two vowels; e.g.,
    *camisa* /kamiza/ 'shirt')
11. Word-final *z* is pronounced /s/ (e.g., *luz* /lus/ 'light')
12. *ss* is pronounced /s/; (*interesse* /inteɾese/ 'interest')

## The assignment

Compile an FST that implements the above rules, then develop unit tests for it.

## What to do

In [`g2p.py`](g2p.py), use `pynini.cdrewrite` to implement each of the above
rules. Then compose them to define the constant `G2P`. For instance, the
following would implement rules 8 and 9:

``` {.python}
G2P = (
    pynini.cdrewrite(pynini.cross("lh", "ʎ"), "", "", SIGMA_STAR) @
    pynini.cdrewrite(pynini.cross("nh", "ɲ"), "", "", SIGMA_STAR)
)
```

### Hints

1.  First, write the tests in [`g2p_test.py`](g2p_test.py). A helper method and
    one example are given there.
2.  Then, in [`g2p.py`](g2p.py) define `SIGMA_STAR`.
4.  Then, then write the first rule, and run the tests as follows, to see how
    much more you have to do: `python g2p_test.py`.
4.  If you see a "Composition failure" error, you likely have omitted some
    grapheme or phoneme in `SIGMA_STAR`.
5.  "Word-finality" is indicated by the string `"[EOS]"`, short for "end of
    string".
6.  Depending on how you write the rules, it may be necessary to attend to their
    ordering to get the right answer. For instance, you don't want to delete *h*
    until you've taken care of *ch*, *lh*, and *nh*.
7.  Use `black`, `flake8`, and `mypy` to make your code beautiful.
8.  When all the tests pass, you're done.

### What to turn in

1.  Your final `g2p.py` and `g2p_test.py`, with the TODOs completed and removed.
2.  A one-page write-up, in PDF form, detailing any challenges you experienced
    and how you dealt with them.

## Stretch goals

1.  The following mini-corpus shows the behavior of *á*, *r*, *rr* and certain
    affricates. Revise your rules to handle these examples, and add appropriate
    tests.

        árvore arvoɾe
        braço bɾasu
        carro kaʁu
        interesse inteɾese
        partes paɾtʃis
        rápido ʁapidu
        verdade veɾdadʒi

2.  Try to make your rules more DRY. For instance, you may be able to combine
    rules 1-2 or 8-9 so that both rules are a single `cdrewrite`.

## References

Beesley, K. R., and Karttunen, Lauri. 2003. *Finite State Morphology*. CSLI
Publications.
