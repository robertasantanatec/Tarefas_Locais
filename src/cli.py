"""Interface de linha de comando em português."""

import argparse
import sqlite3
import sys

from . import __version__
from .config import caminho_banco
from .observabilidade import registrar
from .tarefas import RepositorioTarefas


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Organize tarefas locais com persistência em SQLite."
    )
    parser.add_argument("--version", action="version", version=f"Tarefas Locais {__version__}")
    parser.add_argument("--banco", default=None, help="caminho do banco SQLite")
    comandos = parser.add_subparsers(dest="comando", required=True)

    adicionar = comandos.add_parser("adicionar", help="cadastrar uma tarefa pendente")
    adicionar.add_argument("titulo", help="título entre aspas, com 1 a 120 caracteres")
    listar = comandos.add_parser("listar", help="listar tarefas por identificador")
    listar.add_argument("--status", choices=["todas", "pendentes", "concluidas"], default="todas")
    concluir = comandos.add_parser("concluir", help="marcar uma tarefa como concluída")
    concluir.add_argument("id", type=int)
    excluir = comandos.add_parser("excluir", help="excluir uma tarefa com confirmação explícita")
    excluir.add_argument("id", type=int)
    excluir.add_argument("--confirmar", action="store_true", help="confirmar a exclusão permanente")
    editar = comandos.add_parser("editar", help="alterar o título preservando ID e situação")
    editar.add_argument("id", type=int)
    editar.add_argument("titulo")
    reabrir = comandos.add_parser("reabrir", help="voltar uma tarefa à situação pendente")
    reabrir.add_argument("id", type=int)
    return parser


def main(argumentos: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argumentos)
    if args.comando == "excluir" and not args.confirmar:
        registrar("WARNING", "confirmacao_ausente", args.comando, args.id)
        print("Exclusão não confirmada. Repita o comando com --confirmar.", file=sys.stderr)
        return 1
    try:
        repositorio = RepositorioTarefas(caminho_banco(args.banco))
        if args.comando == "adicionar":
            tarefa = repositorio.adicionar(args.titulo)
            print(f"Tarefa {tarefa.id} cadastrada como pendente: {tarefa.titulo}")
        elif args.comando == "listar":
            tarefas = repositorio.listar(args.status)
            if not tarefas:
                print("Nenhuma tarefa encontrada.")
            else:
                print("ID | Status | Título")
                for tarefa in tarefas:
                    status = "Concluída" if tarefa.concluida else "Pendente"
                    print(f"{tarefa.id} | {status} | {tarefa.titulo}")
        elif args.comando == "concluir":
            alterada = repositorio.concluir(args.id)
            print(
                f"Tarefa {args.id} concluída."
                if alterada
                else f"A tarefa {args.id} já estava concluída."
            )
        elif args.comando == "editar":
            tarefa = repositorio.editar(args.id, args.titulo)
            print(f"Tarefa {tarefa.id} atualizada: {tarefa.titulo}")
        elif args.comando == "reabrir":
            alterada = repositorio.reabrir(args.id)
            print(
                f"Tarefa {args.id} reaberta como pendente."
                if alterada
                else f"A tarefa {args.id} já estava pendente."
            )
        elif args.comando == "excluir":
            repositorio.excluir(args.id)
            print(f"Tarefa {args.id} excluída.")
    except ValueError as erro:
        registrar(
            "WARNING",
            "validacao_falhou",
            args.comando,
            getattr(args, "id", None),
            type(erro).__name__,
        )
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    except (sqlite3.Error, OSError) as erro:
        registrar(
            "ERROR",
            "banco_indisponivel",
            args.comando,
            getattr(args, "id", None),
            type(erro).__name__,
        )
        print(f"Não foi possível acessar o banco de dados: {erro}", file=sys.stderr)
        return 1
    registrar("INFO", "comando_concluido", args.comando, getattr(args, "id", None))
    return 0
