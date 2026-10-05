"""Agregações básicas sobre os votos nominais por candidato."""

import pandas as pd


def votos_por_candidato(df: pd.DataFrame, cargo: str) -> pd.DataFrame:
    """Total de votos e percentual de votos nominais por candidato em um cargo."""
    sub = df[df["DS_CARGO"].str.upper() == cargo.upper()]
    tot = (
        sub.groupby(["NM_URNA_CANDIDATO", "SG_PARTIDO"], as_index=False)["QT_VOTOS_NOMINAIS"]
        .sum()
        .sort_values("QT_VOTOS_NOMINAIS", ascending=False)
        .reset_index(drop=True)
    )
    tot["PERCENTUAL"] = 100 * tot["QT_VOTOS_NOMINAIS"] / tot["QT_VOTOS_NOMINAIS"].sum()
    return tot


def votos_por_uf(df: pd.DataFrame, cargo: str) -> pd.DataFrame:
    """Votos por candidato em cada UF (tabela UF x candidato)."""
    sub = df[df["DS_CARGO"].str.upper() == cargo.upper()]
    return sub.pivot_table(
        index="SG_UF",
        columns="NM_URNA_CANDIDATO",
        values="QT_VOTOS_NOMINAIS",
        aggfunc="sum",
        fill_value=0,
    )
