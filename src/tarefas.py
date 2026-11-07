"""Regras de tarefas e persistência em SQLite, sem dependências externas."""

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


class TarefaNaoEncontrada(ValueError):
    """Identificador válido que não existe na base."""


@dataclass(frozen=True)
class Tarefa:
    id: int
    titulo: str
    concluida: bool


class RepositorioTarefas:
    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)

    @contextmanager
    def _conectar(self):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        conexao = sqlite3.connect(self.caminho, timeout=5)
        try:
            with conexao:
                conexao.execute(
                    """CREATE TABLE IF NOT EXISTS tarefas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL CHECK(length(titulo) BETWEEN 1 AND 120),
                        concluida INTEGER NOT NULL DEFAULT 0 CHECK(concluida IN (0, 1))
                    )"""
                )
                yield conexao
        finally:
            conexao.close()

    @staticmethod
    def _validar_id(identificador: int):
        if isinstance(identificador, bool) or not isinstance(identificador, int) or identificador <= 0:
            raise ValueError("O identificador deve ser um inteiro maior que zero.")

    def adicionar(self, titulo: str) -> Tarefa:
        if not isinstance(titulo, str):
            raise ValueError("O título deve ser um texto.")
        titulo = " ".join(titulo.split())
        if not 1 <= len(titulo) <= 120:
            raise ValueError("O título deve ter entre 1 e 120 caracteres após normalizar os espaços.")
        if not titulo.isprintable():
            raise ValueError("O título deve conter apenas texto imprimível.")
        with self._conectar() as conexao:
            cursor = conexao.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
            identificador = cursor.lastrowid
        return Tarefa(identificador, titulo, False)

    def listar(self, status: str = "todas") -> list[Tarefa]:
        if status not in {"todas", "pendentes", "concluidas"}:
            raise ValueError("Filtro inválido. Use todas, pendentes ou concluidas.")
        with self._conectar() as conexao:
            if status == "todas":
                linhas = conexao.execute("SELECT id, titulo, concluida FROM tarefas ORDER BY id").fetchall()
            else:
                linhas = conexao.execute(
                    "SELECT id, titulo, concluida FROM tarefas WHERE concluida = ? ORDER BY id",
                    (int(status == "concluidas"),),
                ).fetchall()
        return [Tarefa(id_, titulo, bool(concluida)) for id_, titulo, concluida in linhas]

    def concluir(self, identificador: int) -> bool:
        """Retorna True na primeira conclusão e False quando já estava concluída."""
        self._validar_id(identificador)
        with self._conectar() as conexao:
            cursor = conexao.execute(
                "UPDATE tarefas SET concluida = 1 WHERE id = ? AND concluida = 0",
                (identificador,),
            )
            if cursor.rowcount:
                return True
            if conexao.execute("SELECT id FROM tarefas WHERE id = ?", (identificador,)).fetchone():
                return False
            raise TarefaNaoEncontrada(f"Tarefa {identificador} não encontrada.")

    def excluir(self, identificador: int):
        self._validar_id(identificador)
        with self._conectar() as conexao:
            cursor = conexao.execute("DELETE FROM tarefas WHERE id = ?", (identificador,))
            if not cursor.rowcount:
                raise TarefaNaoEncontrada(f"Tarefa {identificador} não encontrada.")
