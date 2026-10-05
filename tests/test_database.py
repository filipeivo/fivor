import sqlite3
import zipfile

import pandas as pd

from eleicoes2026 import database


def _linhas(uf, registros):
    base = {
        "NR_TURNO": 1, "DS_SIT_TOT_TURNO": "#NULO#", "NM_CANDIDATO": "", "NR_CANDIDATO": 0,
        "SG_MUNICIPIO": "X",
    }
    return pd.DataFrame([{**base, **r, "SG_UF": uf} for r in registros])


def _zip(tmp_path):
    pres = {"SQ_CANDIDATO": 1, "SG_UE": "BR", "DS_CARGO": "Presidente",
            "NM_URNA_CANDIDATO": "ANA", "SG_PARTIDO": "P1"}
    gov_sp = {"SQ_CANDIDATO": 2, "SG_UE": "SP", "DS_CARGO": "Governador",
              "NM_URNA_CANDIDATO": "BIA", "SG_PARTIDO": "P2"}
    sp = _linhas("SP", [{**pres, "QT_VOTOS_NOMINAIS": 10}, {**pres, "QT_VOTOS_NOMINAIS": 5},
                        {**gov_sp, "QT_VOTOS_NOMINAIS": 7},
                        {**gov_sp, "NR_TURNO": 2, "QT_VOTOS_NOMINAIS": 100}])
    rj = _linhas("RJ", [{**pres, "QT_VOTOS_NOMINAIS": 20}])
    br = _linhas("BR", [{**pres, "QT_VOTOS_NOMINAIS": 999}])  # deve ser ignorado
    arq = tmp_path / "votacao_candidato_munzona_2026.zip"
    with zipfile.ZipFile(arq, "w") as z:
        for uf, df in {"SP": sp, "RJ": rj, "BRASIL": br}.items():
            z.writestr(f"votacao_candidato_munzona_2026_{uf}.csv",
                       df.to_csv(sep=";", index=False).encode("latin-1"))
    return arq


def test_construir_soma_por_candidato(tmp_path):
    base = database.construir(_zip(tmp_path))
    votos = dict(zip(base["nm_urna_candidato"], base["qt_votos_nominais"]))
    assert votos == {"ANA": 35, "BIA": 7}
    assert {"nm_candidato", "sg_partido", "ds_cargo", "qt_votos_nominais"} <= set(base.columns)


def test_salvar_sqlite_e_csv(tmp_path):
    base = database.construir(_zip(tmp_path))
    db, csv = database.salvar(base, tmp_path / "out")
    with sqlite3.connect(db) as con:
        assert con.execute("SELECT SUM(qt_votos_nominais) FROM votos_candidatos").fetchone()[0] == 42
    assert csv.exists()
