"""Baseline reproduzível; usa somente um banco temporário."""

import json
import math
import platform
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from time import perf_counter

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from src.tarefas import RepositorioTarefas  # noqa: E402


def main():
    resultados = {}
    with tempfile.TemporaryDirectory() as pasta:
        banco = Path(pasta) / "carga.sqlite3"
        repo = RepositorioTarefas(banco)
        for i in range(1000):
            repo.adicionar(f"Carga {i}")
        operacoes = {
            "adicionar": lambda: repo.adicionar("Amostra"),
            "listar_1000": repo.listar,
            "editar": lambda: repo.editar(1, "Editada"),
            "concluir_reabrir": lambda: (repo.concluir(1), repo.reabrir(1)),
            "adicionar_excluir": lambda: repo.excluir(repo.adicionar("Remover").id),
            "cli_listar": lambda: subprocess.run(
                [sys.executable, "-m", "src", "--banco", str(banco), "listar"],
                cwd=RAIZ,
                capture_output=True,
                check=True,
            ),
        }
        for nome, executar in operacoes.items():
            executar()  # aquecimento, fora das amostras
            tempos = []
            for _ in range(30):
                inicio = perf_counter()
                executar()
                tempos.append((perf_counter() - inicio) * 1000)
            p95 = sorted(tempos)[math.ceil(0.95 * len(tempos)) - 1]
            resultados[nome] = {
                "mediana_ms": round(statistics.median(tempos), 3),
                "p95_ms": round(p95, 3),
                "atende_rnf08": p95 < 1000,
            }
    print(
        json.dumps(
            {
                "python": platform.python_version(),
                "plataforma": platform.platform(),
                "volume_inicial": 1000,
                "repeticoes": 30,
                "limite_p95_ms": 1000,
                "resultados": resultados,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all(r["atende_rnf08"] for r in resultados.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
