"""Configuração local: argumento > ambiente do processo > .env > padrão."""

import os
from pathlib import Path

from dotenv import dotenv_values


def caminho_banco(explicito: str | None = None, arquivo: Path | None = None) -> str:
    if explicito is not None:
        return explicito
    valores = dotenv_values(
        arquivo or Path(__file__).resolve().parents[1] / ".env", interpolate=False
    )
    valor = os.environ.get("TAREFAS_BANCO", valores.get("TAREFAS_BANCO"))
    if valor is not None and not valor.strip():
        raise ValueError("TAREFAS_BANCO não pode ser vazio. Informe um caminho SQLite.")
    return valor or "data/tarefas.sqlite3"
