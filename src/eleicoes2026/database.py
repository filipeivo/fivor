"""Base de dados com o total de votos de todos os candidatos do Brasil (1º turno).

Lê todos os CSVs por UF do .zip `votacao_candidato_munzona_2026` do TSE,
soma os votos de cada candidato (municípios e zonas) e grava em SQLite e CSV.
"""

import sqlite3
import zipfile
from pathlib import Path

import pandas as pd

from . import TURNO

TABELA = "votos_candidatos"

COLUNAS = [
    "SQ_CANDIDATO",
    "NR_TURNO",
    "SG_UE",  # unidade eleitoral: 'BR' para Presidente, UF para os demais cargos
    "DS_CARGO",
    "NR_CANDIDATO",
    "NM_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "SG_PARTIDO",
    "DS_SIT_TOT_TURNO",
    "QT_VOTOS_NOMINAIS",
]
CHAVE = COLUNAS[:-1]


def _csvs_por_uf(arquivo: Path):
    """Itera os CSVs de cada UF (ignora o arquivo consolidado BRASIL)."""
    with zipfile.ZipFile(arquivo) as z:
        for nome in z.namelist():
            if nome.endswith(".csv") and not nome.endswith("_BRASIL.csv"):
                with z.open(nome) as f:
                    yield pd.read_csv(
                        f, sep=";", encoding="latin-1", usecols=COLUNAS, low_memory=False
                    )


def agregar(df: pd.DataFrame, turno: int = TURNO) -> pd.DataFrame:
    """Soma os votos nominais por candidato no turno informado."""
    df = df[df["NR_TURNO"] == turno]
    return df.groupby(CHAVE, as_index=False, dropna=False)["QT_VOTOS_NOMINAIS"].sum()


def construir(arquivo_zip: Path, turno: int = TURNO) -> pd.DataFrame:
    """Monta a tabela final com um registro por candidato."""
    # Agrega cada UF antes de concatenar para não carregar o arquivo inteiro em memória
    parciais = [agregar(df, turno) for df in _csvs_por_uf(arquivo_zip)]
    # Presidente aparece em todas as UFs: re-agrega para somar o total nacional
    base = agregar(pd.concat(parciais, ignore_index=True), turno)
    base = base.rename(columns={c: c.lower() for c in base.columns})
    return base.sort_values(
        ["sg_ue", "ds_cargo", "qt_votos_nominais"], ascending=[True, True, False]
    ).reset_index(drop=True)


def salvar(base: pd.DataFrame, destino: Path = Path("data/processed")) -> tuple[Path, Path]:
    """Grava a base em SQLite (`eleicoes2026.db`) e CSV."""
    destino.mkdir(parents=True, exist_ok=True)
    db = destino / "eleicoes2026.db"
    csv = destino / f"{TABELA}_2026_t{TURNO}.csv"
    with sqlite3.connect(db) as con:
        base.to_sql(TABELA, con, if_exists="replace", index=False)
        con.execute(f"CREATE INDEX IF NOT EXISTS idx_cargo ON {TABELA}(ds_cargo, sg_ue)")
        con.execute(f"CREATE INDEX IF NOT EXISTS idx_partido ON {TABELA}(sg_partido)")
    base.to_csv(csv, index=False, sep=";", encoding="utf-8")
    return db, csv
