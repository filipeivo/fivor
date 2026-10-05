"""Leitura dos CSVs do TSE (separador ';', encoding latin-1)."""

import zipfile
from pathlib import Path

import pandas as pd

from . import TURNO


def ler_zip(arquivo: Path, uf: str = "BRASIL") -> pd.DataFrame:
    """Lê o CSV de uma UF (ou 'BRASIL') de dentro do .zip do TSE."""
    with zipfile.ZipFile(arquivo) as z:
        nomes = [n for n in z.namelist() if n.endswith(f"_{uf}.csv")]
        if not nomes:
            raise FileNotFoundError(f"CSV da UF {uf} não encontrado em {arquivo}")
        with z.open(nomes[0]) as f:
            return pd.read_csv(f, sep=";", encoding="latin-1", low_memory=False)


def filtrar_turno(df: pd.DataFrame, turno: int = TURNO) -> pd.DataFrame:
    return df[df["NR_TURNO"] == turno]
