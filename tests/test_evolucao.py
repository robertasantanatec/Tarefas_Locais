import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.cli import main
from src.config import caminho_banco
from src.tarefas import RepositorioTarefas, TarefaNaoEncontrada


class TestEvolucao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.banco = Path(self.tmp.name) / "teste.sqlite3"
        self.repo = RepositorioTarefas(self.banco)

    def test_editar_preserva_id_estado_e_outros_registros(self):
        a = self.repo.adicionar("Antigo")
        b = self.repo.adicionar("Outra")
        self.repo.concluir(a.id)
        editada = self.repo.editar(a.id, " Novo   título ")
        self.assertEqual(
            (editada.id, editada.titulo, editada.concluida), (a.id, "Novo título", True)
        )
        self.assertEqual(RepositorioTarefas(self.banco).listar(), [editada, b])

    def test_editar_rejeita_invalidos_sem_alterar_registros(self):
        original = self.repo.adicionar("Manter")
        for titulo in [None, "", " " * 4, "x" * 121, "a\x00b"]:
            with self.subTest(titulo=titulo), self.assertRaises(ValueError):
                self.repo.editar(original.id, titulo)
        for identificador in [0, -1, True, "1", 99]:
            with self.subTest(id=identificador), self.assertRaises(ValueError):
                self.repo.editar(identificador, "Não alterar")
        self.assertEqual(self.repo.listar(), [original])

    def test_editar_limites_e_sql_parametrizado(self):
        a = self.repo.adicionar("Inicial")
        for titulo in ["x", "x" * 120, "'; DROP TABLE tarefas; --"]:
            self.assertEqual(self.repo.editar(a.id, titulo).titulo, titulo)
        self.assertEqual(len(self.repo.listar()), 1)

    def test_reabrir_persiste_sem_afetar_outros(self):
        a = self.repo.adicionar("Voltar")
        b = self.repo.adicionar("Outra")
        self.repo.concluir(a.id)
        self.assertTrue(self.repo.reabrir(a.id))
        self.assertEqual(RepositorioTarefas(self.banco).listar(), [a, b])
        self.assertFalse(self.repo.reabrir(a.id))
        self.assertEqual(self.repo.listar("concluidas"), [])

    def test_reabrir_invalido_e_inexistente_preserva_dados(self):
        a = self.repo.adicionar("Preservar")
        for identificador in [0, -1, True, "1"]:
            with self.subTest(id=identificador), self.assertRaises(ValueError):
                self.repo.reabrir(identificador)
        with self.assertRaises(TarefaNaoEncontrada):
            self.repo.reabrir(99)
        self.assertEqual(self.repo.listar(), [a])

    def test_cli_editar_reabrir_e_logs_json_sem_titulo(self):
        a = self.repo.adicionar("Título privado")
        self.repo.concluir(a.id)
        for comando in [
            ["editar", str(a.id), "Novo privado"],
            ["reabrir", str(a.id)],
            ["reabrir", str(a.id)],
        ]:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(main(["--banco", str(self.banco), *comando]), 0)
            evento = json.loads(err.getvalue())
            self.assertEqual(evento["level"], "INFO")
            self.assertEqual(evento["task_id"], a.id)
            self.assertNotIn("privado", err.getvalue())
        self.assertFalse(self.repo.listar()[0].concluida)

    def test_logs_de_erro_tem_identificador_e_contexto(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(main(["--banco", str(self.banco), "editar", "99", "Privado"]), 1)
        evento = json.loads(err.getvalue().splitlines()[0])
        self.assertEqual(evento["task_id"], 99)
        self.assertEqual(evento["error_type"], "TarefaNaoEncontrada")
        self.assertEqual(evento["command"], "editar")
        self.assertNotIn("Privado", err.getvalue())

    def test_configuracao_precedencia_env_e_exemplo(self):
        env = Path(self.tmp.name) / ".env"
        env.write_text("TAREFAS_BANCO=data/config.sqlite3\n")
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(caminho_banco(arquivo=env), "data/config.sqlite3")
            os.environ["TAREFAS_BANCO"] = "data/sistema.sqlite3"
            self.assertEqual(caminho_banco(arquivo=env), "data/sistema.sqlite3")
            self.assertEqual(caminho_banco("manual.sqlite3", env), "manual.sqlite3")
            os.environ["TAREFAS_BANCO"] = " "
            with self.assertRaises(ValueError):
                caminho_banco(arquivo=env)
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(caminho_banco(arquivo=env.parent / "ausente"), "data/tarefas.sqlite3")
            exemplo = Path(__file__).resolve().parents[1] / ".env.example"
            self.assertEqual(caminho_banco(arquivo=exemplo), "data/tarefas.sqlite3")
