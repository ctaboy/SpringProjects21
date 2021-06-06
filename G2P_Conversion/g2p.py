"""Portuguese g2p rules."""

import pynini
from pynini.lib import rewrite
from pynini.lib import pynutil

v = pynini.union("a", "e", "i", "o", "u")
acute_a = pynini.union("á")
c = pynini.union(
    "b",
    "c",
    "ç",
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
)
p = pynini.union("ʃ", "ʎ", "ɲ", "ɾ", "ʁ", "dʒ")

SIGMA_STAR = pynini.union(v, acute_a, c, p).closure().optimize()

G2P = (
    pynini.cdrewrite(
        pynini.cross("c", "ʃ")
        | pynini.cross("l", "ʎ")
        | pynini.cross("n", "ɲ"),
        "",
        "h",
        SIGMA_STAR,
    )
    @ pynini.cdrewrite(pynutil.delete("h"), "", "", SIGMA_STAR)
    @ pynini.cdrewrite(
        pynini.cross("e", "i") | pynini.cross("o", "u"),
        "",
        pynini.union("[EOS]", "s[EOS]"),
        SIGMA_STAR,
    )
    @ pynini.cdrewrite(pynini.cross("o", "u"), "v", "r", SIGMA_STAR)
    @ pynini.cdrewrite(
        pynini.cross("c", "s"), "", pynini.union("i", "e"), SIGMA_STAR
    )
    @ pynini.cdrewrite(pynini.cross("c", "k"), "", "", SIGMA_STAR)
    @ pynini.cdrewrite(pynini.cross("s", "z"), v, v, SIGMA_STAR)
    @ pynini.cdrewrite(
        pynini.cross(pynini.union("ç", "ss"), "s"), "", "", SIGMA_STAR
    )
    @ pynini.cdrewrite(pynini.cross("z", "s"), "", "[EOS]", SIGMA_STAR)
    @ pynini.cdrewrite(pynini.cross("rr", "ʁ"), "", "", SIGMA_STAR)
    @ pynini.cdrewrite(pynini.cross("r", "ʁ"), "[BOS]", "", SIGMA_STAR)
    @ pynini.cdrewrite(
        pynini.cross("r", "ɾ"),
        pynini.union(c, v),
        pynini.union(c, v),
        SIGMA_STAR,
    )
    @ pynini.cdrewrite(pynini.cross(acute_a, "a"), "", "", SIGMA_STAR)
    @ pynini.cdrewrite(
        pynini.cross("t", "tʃ") | pynini.cross("d", "dʒ"), "", "i", SIGMA_STAR
    )
)


def g2p(istring: str) -> str:
    return rewrite.one_top_rewrite(istring, G2P)
