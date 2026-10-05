"""Download dos arquivos de votação do Portal de Dados Abertos do TSE."""

from pathlib import Path

import requests

BASE_URL = "https://cdn.tse.jus.br/estatistica/sead/odsele"

# Conjuntos de dados do TSE usados no projeto
DATASETS = {
    "candidato_munzona": "votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip",
    "partido_munzona": "votacao_partido_munzona/votacao_partido_munzona_{ano}.zip",
    "detalhe_munzona": "detalhe_votacao_munzona/detalhe_votacao_munzona_{ano}.zip",
}


def url_dataset(nome: str, ano: int = 2026) -> str:
    return f"{BASE_URL}/{DATASETS[nome].format(ano=ano)}"


def baixar(nome: str, destino: Path = Path("data/raw"), ano: int = 2026) -> Path:
    """Baixa o .zip do dataset para `destino` e retorna o caminho do arquivo."""
    destino.mkdir(parents=True, exist_ok=True)
    url = url_dataset(nome, ano)
    arquivo = destino / url.rsplit("/", 1)[-1]
    with requests.get(url, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        with open(arquivo, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    return arquivo
