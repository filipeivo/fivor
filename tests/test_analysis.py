import pandas as pd

from eleicoes2026.analysis import votos_por_candidato, votos_por_uf
from eleicoes2026.download import url_dataset
from eleicoes2026.load import filtrar_turno


def _df():
    return pd.DataFrame(
        {
            "NR_TURNO": [1, 1, 1, 2],
            "SG_UF": ["SP", "RJ", "SP", "SP"],
            "DS_CARGO": ["Presidente"] * 4,
            "NM_URNA_CANDIDATO": ["A", "A", "B", "A"],
            "SG_PARTIDO": ["P1", "P1", "P2", "P1"],
            "QT_VOTOS_NOMINAIS": [60, 15, 25, 999],
        }
    )


def test_votos_por_candidato():
    res = votos_por_candidato(filtrar_turno(_df()), "presidente")
    assert list(res["NM_URNA_CANDIDATO"]) == ["A", "B"]
    assert list(res["PERCENTUAL"]) == [75.0, 25.0]


def test_votos_por_uf():
    res = votos_por_uf(filtrar_turno(_df()), "Presidente")
    assert res.loc["SP", "A"] == 60 and res.loc["RJ", "B"] == 0


def test_url_dataset():
    assert url_dataset("candidato_munzona").endswith("votacao_candidato_munzona_2026.zip")
