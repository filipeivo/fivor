# Eleições 2026 — Análise de votos do 1º turno

Projeto para análise dos votos do **1º turno das eleições gerais brasileiras de 2026** (04/10/2026), usando os dados abertos do [TSE](https://dadosabertos.tse.jus.br/).

## Estrutura

```
src/eleicoes2026/
  download.py   # baixa os .zip do CDN do TSE
  load.py       # lê os CSVs (sep ';', latin-1) e filtra o turno
  analysis.py   # agregações: votos por candidato, por UF
  database.py   # base com os votos de todos os candidatos (SQLite + CSV)
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

# base com todos os candidatos do Brasil -> data/processed/eleicoes2026.db (+ CSV)
eleicoes2026 base

# resultado nacional para Presidente
eleicoes2026 resultado --cargo Presidente

# Governador em SP usando um .zip já baixado
eleicoes2026 resultado --uf SP --cargo Governador --zip data/raw/votacao_candidato_munzona_2026.zip

pytest
```

## Base de dados `votos_candidatos`

Um registro por candidato (1º turno), somando todos os municípios/zonas:

| coluna | descrição |
|---|---|
| sq_candidato | id do candidato no TSE |
| sg_ue | `BR` (Presidente) ou UF (demais cargos) |
| ds_cargo | cargo eletivo |
| nr_candidato | número na urna |
| nm_candidato / nm_urna_candidato | nome civil / nome de urna |
| sg_partido | partido |
| ds_sit_tot_turno | situação (eleito, 2º turno, não eleito...) |
| qt_votos_nominais | quantidade de votos |

```sql
SELECT nm_urna_candidato, sg_partido, qt_votos_nominais
FROM votos_candidatos WHERE ds_cargo = 'Deputado Federal' AND sg_ue = 'SP'
ORDER BY qt_votos_nominais DESC LIMIT 10;
```

> Os arquivos de 2026 são publicados pelo TSE após a totalização; a URL segue o padrão dos anos anteriores e pode precisar de ajuste.
