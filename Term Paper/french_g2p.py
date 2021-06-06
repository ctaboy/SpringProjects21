"""French g2p conversion rules."""

import pynini
from pynini.lib import rewrite
from pynini.lib import pynutil

v = pynini.union(
    "a",
    "e",
    "i",
    "o",
    "u",
    "ɑ̃",
    "â",
    "œ",
    "ɛ",
    "ɛ̃",
    "è",
    "é",
    "ê",
    "ï",
    "î",
    "ô",
    "û",
)
fr_vowels = pynini.union("e", "é", "i", "y")
c = pynini.union(
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "y",
    "z",
    "ç",
    "ʁ",
    "ʃ",
    "ʒ",
    "ɲ",
    "ɔ̃",
    "ɔ",
)


SIGMA_STAR = pynini.union(v, c, fr_vowels).closure().optimize()

G2P = (
    # final d is silent
    pynini.cdrewrite(pynutil.delete("d"), "", "[EOS]", SIGMA_STAR)
    # final e is silent
    @ pynini.cdrewrite(pynutil.delete("e"), "", "[EOS]", SIGMA_STAR)
    # final -er -> e
    @ pynini.cdrewrite(pynutil.delete("r"), "e", "[EOS]", SIGMA_STAR)
    # r -> ʁ
    @ pynini.cdrewrite(pynini.cross("r", "ʁ"), "", "", SIGMA_STAR)
    # ch to k for greek words
    @ pynini.cdrewrite(pynini.cross("ch", "k"), "[BOS]", "aos", SIGMA_STAR)
    # final s is silent
    @ pynini.cdrewrite(pynutil.delete("s"), "", "[EOS]", SIGMA_STAR)
    # b -> p before s, t
    @ pynini.cdrewrite(
        pynini.cross("b", "p"), "", pynini.union("s", "t"), SIGMA_STAR
    )
    # ch to ∫
    @ pynini.cdrewrite(pynini.cross("ch", "ʃ"), "", "", SIGMA_STAR)
    # c -> s before front vowels e, i, y
    @ pynini.cdrewrite(pynini.cross("c", "s"), "", fr_vowels, SIGMA_STAR)
    # cc -> ks before front vowels e, i, y
    @ pynini.cdrewrite(pynini.cross("cc", "ks"), "", fr_vowels, SIGMA_STAR)
    # final c after n is silent
    @ pynini.cdrewrite(pynutil.delete("c"), "n", "[EOS]", SIGMA_STAR)
    # final c -> k
    @ pynini.cdrewrite(
        pynini.cross("c", "k"),
        "",
        pynini.union(fr_vowels, "[EOS]"),
        SIGMA_STAR,
    )
    # c -> k before consonant
    @ pynini.cdrewrite(pynini.cross("c", "k"), "", c, SIGMA_STAR)
    # g -> ʒ
    @ pynini.cdrewrite(pynini.cross("g", "ʒ"), "", fr_vowels, SIGMA_STAR)
    # gn -> ɲ
    @ pynini.cdrewrite(pynini.cross("gn", "ɲ"), "", "", SIGMA_STAR)
    # silent h between vowels
    @ pynini.cdrewrite(pynutil.delete("h"), v, v, SIGMA_STAR)
    # s -> z between vowels
    @ pynini.cdrewrite(pynini.cross("s", "z"), v, v, SIGMA_STAR)
    # final -et -> ɛ
    @ pynini.cdrewrite(pynini.cross("et", "ɛ"), "", "[EOS]", SIGMA_STAR)
    # ent -> ɑ̃ after consonant
    @ pynini.cdrewrite(pynini.cross("ent", "ɑ̃"), c, "[EOS]", SIGMA_STAR)
    # final t is silent
    @ pynini.cdrewrite(pynutil.delete("t"), "", "[EOS]", SIGMA_STAR)
    # th -> t
    @ pynini.cdrewrite(pynini.cross("th", "t"), "", "", SIGMA_STAR)
    # j -> ʒ
    @ pynini.cdrewrite(pynini.cross("j", "ʒ"), "", "", SIGMA_STAR)
    # -ti -> sj when preceded by -on or -ence
    @ pynini.cdrewrite(
        pynini.cross("ti", "sj"), "", pynini.union("on", "ence"), SIGMA_STAR
    )
    # u -> y
    @ pynini.cdrewrite(
        pynini.cross("u", "y"), c, pynini.union("[EOS]", c), SIGMA_STAR
    )
    # ou -> u
    @ pynini.cdrewrite(pynini.cross("ou", "u"), "", "", SIGMA_STAR)
    # oi -> wa
    @ pynini.cdrewrite(pynini.cross("oi", "wa"), "", "", SIGMA_STAR)
    # oy -> waj
    @ pynini.cdrewrite(pynini.cross("oy", "waj"), "", "", SIGMA_STAR)
    # y -> j between vowels
    @ pynini.cdrewrite(pynini.cross("y", "j"), v, v, SIGMA_STAR)
    # u after g/q and before i is silent
    @ pynini.cdrewrite(
        pynutil.delete("u"),
        pynini.union("g", "q"),
        pynini.union("e", "i"),
        SIGMA_STAR,
    )
    # ion/on -> ɔ̃
    @ pynini.cdrewrite(
        pynini.cross("on", "ɔ̃"), pynini.union("i", ""), "[EOS]", SIGMA_STAR
    )
    # o -> ɔ before consonant or vowel
    @ pynini.cdrewrite(pynini.cross("o", "ɔ"), "", "l", SIGMA_STAR)
    # eu -> œ
    @ pynini.cdrewrite(pynini.cross("eu", "œ"), c, c, SIGMA_STAR)
    # a -> ɑ̃
    @ pynini.cdrewrite(
        pynini.cross(pynini.union("an", "am"), "ɑ̃"), "", "[EOS]", SIGMA_STAR
    )
    # è -> ɛ
    @ pynini.cdrewrite(pynini.cross("è", "ɛ"), "", "", SIGMA_STAR)
    # e -> ɛ before consonant cluster ct
    @ pynini.cdrewrite(pynini.cross("e", "ɛ"), c, c, SIGMA_STAR)
    # pp -> p
    @ pynini.cdrewrite(pynini.cross("pp", "p"), "", "", SIGMA_STAR)
    # final x is silent
    @ pynini.cdrewrite(pynutil.delete("x"), "", "[EOS]", SIGMA_STAR)
    # é -> e
    @ pynini.cdrewrite(pynini.cross("é", "e"), "", "", SIGMA_STAR)
    # ll -> j
    @ pynini.cdrewrite(pynini.cross("ll", "j"), "", "", SIGMA_STAR)
)


def g2p(istring: str) -> str:
    return rewrite.one_top_rewrite(istring, G2P)

