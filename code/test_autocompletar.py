import unittest

from dados import gerar_palavras, simular_digitacao
from original import sugerir
from otimizado import Autocompletar


class TestAutocompletar(unittest.TestCase):
    def confere(self, palavras, prefixos):
        indice = Autocompletar(palavras)
        for prefixo in prefixos:
            with self.subTest(prefixo=prefixo):
                self.assertEqual(indice.sugerir(prefixo), sorted(sugerir(palavras, prefixo)))

    def test_digitacao_em_dicionario_gerado(self):
        palavras = gerar_palavras(20_000)
        self.confere(palavras, simular_digitacao(palavras, quantidade=50))

    def test_casos_de_borda(self):
        palavras = ["casa", "casaco", "casa", "caso", "cão", "ação", "a", "Casa", "zebra"]
        self.confere(palavras, ["", "c", "ca", "casa", "casacos", "cã", "a", "C", "x", "zebra", "zz"])

    def test_dicionario_vazio(self):
        self.assertEqual(Autocompletar([]).sugerir("a"), [])


if __name__ == "__main__":
    unittest.main()
