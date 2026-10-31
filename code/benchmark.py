import csv
import time
from bisect import bisect_left
from pathlib import Path

import matplotlib.pyplot as plt

from dados import gerar_palavras, simular_digitacao
from original import sugerir
from otimizado import MAIOR_CARACTERE, Autocompletar

TAMANHOS = [1_000, 10_000, 100_000, 1_000_000]
RESULTADOS = Path(__file__).resolve().parent.parent / "results"


def mede(funcao, *args, repeticoes=3):
    melhor = float("inf")
    for _ in range(repeticoes):
        ini = time.perf_counter()
        funcao(*args)
        melhor = min(melhor, time.perf_counter() - ini)
    return melhor


def consultar_original(palavras, consultas):
    for prefixo in consultas:
        sugerir(palavras, prefixo)


def consultar_otimizado(indice, consultas):
    for prefixo in consultas:
        indice.sugerir(prefixo)


def consultar_so_busca_binaria(indice, consultas):
    for prefixo in consultas:
        inicio = bisect_left(indice.palavras, prefixo)
        bisect_left(indice.palavras, prefixo + MAIOR_CARACTERE, inicio)


def executar():
    linhas = []
    for n in TAMANHOS:
        palavras = gerar_palavras(n)
        consultas = simular_digitacao(palavras)
        indice = Autocompletar(palavras)

        t_original = mede(consultar_original, palavras, consultas)
        t_construcao = mede(Autocompletar, palavras)
        t_otimizado = mede(consultar_otimizado, indice, consultas)
        t_busca = mede(consultar_so_busca_binaria, indice, consultas)

        linha = {
            "n": n,
            "consultas": len(consultas),
            "media_sugestoes": sum(len(indice.sugerir(p)) for p in consultas) / len(consultas),
            "original_ms_por_tecla": t_original / len(consultas) * 1000,
            "otimizado_ms_por_tecla": t_otimizado / len(consultas) * 1000,
            "so_busca_binaria_ms_por_tecla": t_busca / len(consultas) * 1000,
            "construcao_indice_ms": t_construcao * 1000,
            "ganho": t_original / t_otimizado,
        }
        linhas.append(linha)
        print(
            f"n={n:>9,}  original={linha['original_ms_por_tecla']:10.4f} ms/tecla  "
            f"otimizado={linha['otimizado_ms_por_tecla']:8.4f} ms/tecla  "
            f"índice={linha['construcao_indice_ms']:9.2f} ms  ganho={linha['ganho']:8.1f}x  "
            f"sugestões/tecla={linha['media_sugestoes']:8.1f}"
        )
    return linhas


def salvar_csv(linhas, caminho=RESULTADOS / "resultados.csv"):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
        escritor.writeheader()
        escritor.writerows(linhas)


def salvar_grafico(linhas, caminho=RESULTADOS / "grafico.png"):
    ns = [linha["n"] for linha in linhas]
    plt.figure(figsize=(7, 4.2))
    plt.loglog(ns, [linha["original_ms_por_tecla"] for linha in linhas], "o-", label="Original (varredura linear)")
    plt.loglog(ns, [linha["otimizado_ms_por_tecla"] for linha in linhas], "s-", label="Otimizado (lista ordenada + bisect)")
    plt.xlabel("Tamanho do dicionário (palavras)")
    plt.ylabel("Tempo por tecla (ms)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho, dpi=200)


if __name__ == "__main__":
    RESULTADOS.mkdir(exist_ok=True)
    resultados = executar()
    salvar_csv(resultados)
    salvar_grafico(resultados)
