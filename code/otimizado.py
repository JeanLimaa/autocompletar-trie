from bisect import bisect_left

MAIOR_CARACTERE = chr(0x10FFFF)


class Autocompletar:
    def __init__(self, palavras):
        self.palavras = sorted(palavras)

    def sugerir(self, prefixo):
        inicio = bisect_left(self.palavras, prefixo)
        fim = bisect_left(self.palavras, prefixo + MAIOR_CARACTERE, inicio)
        return self.palavras[inicio:fim]
