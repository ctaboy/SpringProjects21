#!/usr/bin/env python
"""Unit tests for French G2P."""

import unittest
import french_g2p


class G2PTest(unittest.TestCase):
    def rewrites(self, istring: str, expected_ostring: str) -> None:
        ostring = french_g2p.g2p(istring)
        self.assertEqual(ostring, expected_ostring)

    def test_appris(self):
        self.rewrites("appris", "apʁi")

    def test_absolu(self):
        self.rewrites("absolu", "apsɔly")

    def test_accident(self):
        self.rewrites("accident", "aksidɑ̃")

    def test_adaptation(self):
        self.rewrites("adaptation", "adaptasjɔ̃")

    def test_croix(self):
        self.rewrites("croix", "kʁwa")

    def test_flanc(self):
        self.rewrites("flanc", "flɑ̃")

    def test_millet(self):
        self.rewrites("millet", "mijɛ")

    def test_arche(self):
        self.rewrites("arche", "aʁʃ")

    def test_chaos(self):
        self.rewrites("chaos", "kao")

    def test_suggerer(self):
        self.rewrites("suggérer", "sygʒeʁe")

    def test_signifie(self):
        self.rewrites("signifie", "siɲifi")

    def test_trahisons(self):
        self.rewrites("trahisons", "tʁaizɔ̃")

    def test_royer(self):
        self.rewrites("royer", "ʁwaje")

    def test_facteurs(self):
        self.rewrites("facteurs", "faktœʁ")

    def test_partout(self):
        self.rewrites("partout", "paʁtu")

    def test_anatheme(self):
        self.rewrites("anathème", "anatɛm")

    def test_disposition(self):
        self.rewrites("disposition", "dispozisjɔ̃")

    def test_trajectoire(self):
        self.rewrites("trajectoire", "tʁaʒɛktwaʁ")

    def test_noyade(self):
        self.rewrites("noyade", "nwajad")

    def test_guichet(self):
        self.rewrites("guichet", "giʃɛ")


if __name__ == "__main__":
    unittest.main()
