import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.banco = Path(self.pasta.name) / "tarefas.sqlite3"

    def executar(self, *argumentos):
        return subprocess.run(
            [sys.executable, "-m", "src", "--banco", str(self.banco), *argumentos],
            cwd=Path(__file__).resolve().parents[1],
            encoding="utf-8", capture_output=True, check=False,
            env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'},
        )

    def test_ciclo_completo_persiste_entre_processos(self):
        self.assertEqual(self.executar("adicionar", "Ler documentação").returncode, 0)
        self.assertIn("Pendente | Ler documentação", self.executar("listar").stdout)
        self.assertEqual(self.executar("concluir", "1").returncode, 0)
        self.assertIn("Concluída", self.executar("listar", "--status", "concluidas").stdout)
        self.assertEqual(self.executar("excluir", "1", "--confirmar").returncode, 0)
        self.assertIn("Nenhuma tarefa", self.executar("listar").stdout)

    def test_excluir_sem_confirmacao_nao_remove(self):
        self.executar("adicionar", "Preservar")
        resultado = self.executar("excluir", "1")
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("--confirmar", resultado.stderr)
        self.assertIn("Preservar", self.executar("listar").stdout)

    def test_ausencia_de_confirmacao_nao_cria_banco(self):
        self.executar("excluir", "1")
        self.assertFalse(self.banco.exists())

    def test_entrada_invalida_retorna_erro_legivel(self):
        resultado = self.executar("adicionar", " ")
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("entre 1 e 120", resultado.stderr)
        self.assertEqual(resultado.stdout, "")

    def test_id_inexistente_retorna_codigo_um(self):
        resultado = self.executar("concluir", "99")
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("não encontrada", resultado.stderr)

    def test_id_nao_numerico_e_filtro_invalido_retornam_codigo_dois(self):
        for argumentos in [("concluir", "abc"), ("listar", "--status", "urgentes")]:
            with self.subTest(argumentos=argumentos):
                self.assertEqual(self.executar(*argumentos).returncode, 2)

    def test_id_nao_positivo_retorna_codigo_um(self):
        self.assertEqual(self.executar("concluir", "0").returncode, 1)

    def test_ajuda_e_versao_nao_criam_banco(self):
        self.assertEqual(self.executar("--help").returncode, 0)
        resultado = self.executar("--version")
        self.assertEqual(resultado.returncode, 0)
        self.assertIn("0.1.0", resultado.stdout)
        self.assertFalse(self.banco.exists())

    def test_caminho_inacessivel_retorna_erro_controlado(self):
        self.banco.mkdir()
        resultado = self.executar("listar")
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("banco de dados", resultado.stderr)
        self.assertNotIn("Traceback", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
