import tempfile
import unittest
from pathlib import Path

from src.tarefas import RepositorioTarefas, TarefaNaoEncontrada


class TestRepositorioTarefas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.banco = Path(self.pasta.name) / "dados" / "tarefas.sqlite3"
        self.repo = RepositorioTarefas(self.banco)

    def test_cadastrar_inicia_pendente_e_normaliza_espacos(self):
        tarefa = self.repo.adicionar("  Ler   sobre SQLite\nhoje  ")
        self.assertEqual(tarefa.titulo, "Ler sobre SQLite hoje")
        self.assertFalse(tarefa.concluida)
        self.assertGreater(tarefa.id, 0)

    def test_aceitar_titulo_com_um_caractere(self):
        self.assertEqual(self.repo.adicionar("A").titulo, "A")

    def test_aceitar_limite_de_120_caracteres(self):
        self.assertEqual(len(self.repo.adicionar("á" * 120).titulo), 120)

    def test_rejeitar_titulos_vazios_ou_longos_sem_criar_registro(self):
        for titulo in ["", "  \t\n ", "a" * 121]:
            with self.subTest(titulo=titulo):
                with self.assertRaises(ValueError):
                    self.repo.adicionar(titulo)
        self.assertEqual(self.repo.listar(), [])

    def test_rejeitar_controle_nao_imprimivel(self):
        with self.assertRaises(ValueError):
            self.repo.adicionar("tarefa\x00oculta")

    def test_listar_sem_registros(self):
        self.assertEqual(self.repo.listar(), [])

    def test_listar_em_ordem_de_identificador(self):
        a = self.repo.adicionar("Primeira")
        b = self.repo.adicionar("Segunda")
        self.assertEqual([t.id for t in self.repo.listar()], [a.id, b.id])

    def test_persistir_entre_instancias(self):
        tarefa = self.repo.adicionar("Continuar amanhã")
        outra = RepositorioTarefas(self.banco)
        self.assertEqual(outra.listar(), [tarefa])

    def test_concluir_altera_apenas_a_tarefa_selecionada(self):
        a = self.repo.adicionar("Estudar")
        b = self.repo.adicionar("Revisar")
        self.assertTrue(self.repo.concluir(a.id))
        self.assertEqual(
            [(t.id, t.concluida) for t in self.repo.listar()], [(a.id, True), (b.id, False)]
        )

    def test_concluir_novamente_e_idempotente(self):
        tarefa = self.repo.adicionar("Revisar PR")
        self.repo.concluir(tarefa.id)
        self.assertFalse(self.repo.concluir(tarefa.id))
        self.assertEqual(len(self.repo.listar()), 1)

    def test_filtrar_pendentes_e_concluidas(self):
        a = self.repo.adicionar("A")
        b = self.repo.adicionar("B")
        self.repo.concluir(a.id)
        self.assertEqual([t.id for t in self.repo.listar("pendentes")], [b.id])
        self.assertEqual([t.id for t in self.repo.listar("concluidas")], [a.id])

    def test_rejeitar_filtro_desconhecido(self):
        with self.assertRaises(ValueError):
            self.repo.listar("urgentes")

    def test_excluir_preserva_as_outras_tarefas(self):
        a = self.repo.adicionar("A")
        b = self.repo.adicionar("B")
        self.repo.excluir(a.id)
        self.assertEqual(self.repo.listar(), [b])

    def test_id_inexistente_nao_modifica_a_base(self):
        tarefa = self.repo.adicionar("Manter")
        for operacao in [self.repo.concluir, self.repo.excluir]:
            with self.subTest(operacao=operacao.__name__):
                with self.assertRaises(TarefaNaoEncontrada):
                    operacao(tarefa.id + 100)
        self.assertEqual(self.repo.listar(), [tarefa])

    def test_rejeitar_identificadores_invalidos(self):
        for id_ in [-1, 0, "1", True]:
            for operacao in [self.repo.concluir, self.repo.excluir]:
                with self.subTest(id=id_, operacao=operacao.__name__):
                    with self.assertRaises(ValueError):
                        operacao(id_)

    def test_texto_parecido_com_sql_permanece_como_titulo(self):
        texto = "Ler SQL'); DROP TABLE tarefas; --"
        tarefa = self.repo.adicionar(texto)
        self.assertEqual(self.repo.listar(), [tarefa])
        self.repo.adicionar("A tabela continua disponível")
        self.assertEqual(len(self.repo.listar()), 2)

    def test_excluir_nao_reutiliza_identificador(self):
        a = self.repo.adicionar("A")
        self.repo.excluir(a.id)
        b = self.repo.adicionar("B")
        self.assertGreater(b.id, a.id)


if __name__ == "__main__":
    unittest.main()
