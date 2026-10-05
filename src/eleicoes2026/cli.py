"""CLI: baixa os dados do TSE, monta a base de votos e imprime resultados."""

import argparse
from pathlib import Path

from . import database
from .analysis import votos_por_candidato
from .download import DATASETS, baixar
from .load import filtrar_turno, ler_zip


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("base", help="monta a base com os votos de todos os candidatos")
    b.add_argument("--zip", type=Path, help="usar .zip já baixado em vez de baixar")
    b.add_argument("--destino", type=Path, default=Path("data/processed"))

    r = sub.add_parser("resultado", help="imprime o resultado de um cargo")
    r.add_argument("--dataset", default="candidato_munzona", choices=DATASETS)
    r.add_argument("--uf", default="BRASIL")
    r.add_argument("--cargo", default="Presidente")
    r.add_argument("--zip", type=Path, help="usar .zip já baixado em vez de baixar")

    args = p.parse_args()
    if args.cmd == "base":
        arquivo = args.zip or baixar("candidato_munzona")
        base = database.construir(arquivo)
        db, csv = database.salvar(base, args.destino)
        print(f"{len(base)} candidatos gravados em {db} e {csv}")
    else:
        arquivo = args.zip or baixar(args.dataset)
        df = filtrar_turno(ler_zip(arquivo, args.uf))
        print(votos_por_candidato(df, args.cargo).to_string(index=False))


if __name__ == "__main__":
    main()
