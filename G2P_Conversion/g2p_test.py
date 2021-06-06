"""Unit tests for Portuguese G2P."""

import unittest
import g2p


class G2PTest(unittest.TestCase):
    def rewrites(self, istring: str, expected_ostring: str) -> None:
        ostring = g2p.g2p(istring)
        self.assertEqual(ostring, expected_ostring)

    # def test_chato(self):
    #     self.rewrites("chato", "ʃatu")
    #
    # def test_filho(self):
    #     self.rewrites("filho", "fiʎu")
    #
    # def test_vermelho(self):
    #     self.rewrites("vermelho", "veɾmeʎu")
    #
    # def test_ninho(self):
    #     self.rewrites("ninho", "niɲu")
    #
    # def test_gatinho(self):
    #     self.rewrites("gatinho", "gatʃiɲu")
    #
    # def test_homem(self):
    #     self.rewrites("homem", "omem")
    #
    # def test_cimento(self):
    #     self.rewrites("cimento", "simentu")
    #
    # def test_casa(self):
    #     self.rewrites("casa", "kaza")
    #
    # def test_interesse(self):
    #     self.rewrites("interesse", "inteɾesi")
    #
    # def test_case_s(self):
    #     self.rewrites("case", "kazi")
    #     self.rewrites("cases", "kazis")
    #
    # def test_verdade(self):
    #     self.rewrites("verdade", "veɾdadʒi")
    #
    # def test_arvore(self):
    #     self.rewrites("árvore", "arvuɾi")
    #
    # def test_braco_s(self):
    #     self.rewrites("braço", "bɾasu")
    #     self.rewrites("braços", "bɾasus")
    #
    # def test_vez(self):
    #     self.rewrites("vez", "ves")
    #
    # def test_luz(self):
    #     self.rewrites("luz", "lus")
    #
    # def test_rapido(self):
    #     self.rewrites("rápido", "ʁapidu")
    #
    # def test_partes(self):
    #     self.rewrites("partes", "paɾtʃis")
    #
    # def test_carro(self):
    #     self.rewrites("carro", "kaʁu")

    def test_all(self):
        test_cases = [
            ("cases", "kazis"),
            ("luz", "lus"),
            ("carro", "kaʁu")
        ]
        for case in test_cases:
            self.rewrites(case[0], case[1])


if __name__ == "__main__":
    unittest.main()
