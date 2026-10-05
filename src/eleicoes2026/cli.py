"""CLI: baixa os dados do TSE e imprime o resultado do 1º turno por cargo."""

import argparse
from pathlib import Path

from .analysis import votos_por_candidato
from .download import DATASETS, baixar
from .load import filtrar_turno, ler_zip


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", default="candidato_munzona", choices=DATASETS)
    p.add_argument("--uf", default="BRASIL")
    p.add_argument("--cargo", default="Presidente")
    p.add_argument("--zip", type=Path, help="usar .zip já baixado em vez de baixar")
    args = p.parse_args()

    arquivo = args.zip or baixar(args.dataset)
    df = filtrar_turno(ler_zip(arquivo, args.uf))
    print(votos_por_candidato(df, args.cargo).to_string(index=False))


if __name__ == "__main__":
    main()
