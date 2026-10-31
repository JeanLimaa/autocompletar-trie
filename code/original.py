def sugerir(palavras, prefixo):
    resultado = []
    for p in palavras:
        if p.startswith(prefixo):
            resultado.append(p)
    return resultado
