# Autocompletar por prefixo: Entrega 1 (Av2)

`code/original.py` Versão original: varredura linear do dicionário a cada tecla
`code/otimizado.py` Primeira otimização: dicionário ordenado + busca binária (`bisect`)
`code/dados.py` Gerador do dicionário sintético e simulação de digitação
`code/test_autocompletar.py` Confere que a versão otimizada devolve as mesmas sugestões da original
`code/benchmark.py` Mede as duas versões e gera `results/resultados.csv` e `results/grafico.png`
`docs/` Relatório da entrega e Documento do projeto

```bash
pip install -r requirements.txt
python -m unittest discover -s code -v
python code/benchmark.py
```
