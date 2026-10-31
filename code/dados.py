import random

CONSOANTES = "bcdfglmnprstv"
VOGAIS = "aeiou"
SILABAS = [c + v for c in CONSOANTES for v in VOGAIS]


def gerar_palavras(n, semente=42):
    rng = random.Random(semente)
    return ["".join(rng.choices(SILABAS, k=rng.randint(2, 5))) for _ in range(n)]


def simular_digitacao(palavras, quantidade=20, semente=7):
    rng = random.Random(semente)
    consultas = []
    for palavra in rng.sample(palavras, quantidade):
        consultas.extend(palavra[:i] for i in range(1, len(palavra) + 1))
    return consultas
