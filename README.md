# Eleições 2026 — Análise de votos do 1º turno

Projeto para análise dos votos do **1º turno das eleições gerais brasileiras de 2026** (04/10/2026), usando os dados abertos do [TSE](https://dadosabertos.tse.jus.br/).

## Estrutura

```
src/eleicoes2026/
  download.py   # baixa os .zip do CDN do TSE
  load.py       # lê os CSVs (sep ';', latin-1) e filtra o turno
  analysis.py   # agregações: votos por candidato, por UF
  cli.py        # linha de comando
data/raw/       # arquivos brutos (não versionados)
data/processed/ # dados tratados (não versionados)
notebooks/      # análises exploratórias
tests/
```

## Uso

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# resultado nacional para Presidente (baixa os dados do TSE)
eleicoes2026 --cargo Presidente

# Governador em SP usando um .zip já baixado
eleicoes2026 --uf SP --cargo Governador --zip data/raw/votacao_candidato_munzona_2026.zip

pytest
```

> Os arquivos de 2026 são publicados pelo TSE após a totalização; a URL segue o padrão dos anos anteriores e pode precisar de ajuste.
