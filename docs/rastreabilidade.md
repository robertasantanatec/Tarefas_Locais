# Matriz de rastreabilidade e validação

## Requisitos funcionais

Os nomes de testes abaixo correspondem aos métodos existentes nos arquivos indicados. A suíte completa deve ser executada antes da integração de mudanças.

| RF | Caso de uso | História | Backlog | Implementação | Testes em `tests/test_tarefas.py` |
|---|---|---|---|---|---|
| RF01 | CU01 | US01 | BL02 | `RepositorioTarefas.adicionar`; comando `adicionar` | `test_cadastrar_inicia_pendente_e_normaliza_espacos`; `test_aceitar_titulo_com_um_caractere`; `test_aceitar_limite_de_120_caracteres`; `test_rejeitar_titulos_vazios_ou_longos_sem_criar_registro`; `test_rejeitar_controle_nao_imprimivel` |
| RF02 | CU02 | US02 | BL03 | `RepositorioTarefas.listar`; comando `listar` | `test_listar_sem_registros`; `test_listar_em_ordem_de_identificador`; `test_filtrar_pendentes_e_concluidas`; `test_rejeitar_filtro_desconhecido` |
| RF03 | CU03 | US03 | BL04 | `RepositorioTarefas.concluir`; comando `concluir` | `test_concluir_altera_apenas_a_tarefa_selecionada`; `test_concluir_novamente_e_idempotente`; `test_id_inexistente_nao_modifica_a_base`; `test_rejeitar_identificadores_invalidos` |
| RF04 | CU04 | US04 | BL05 | `RepositorioTarefas.excluir`; confirmação em `cli.main` | `test_excluir_preserva_as_outras_tarefas`; `test_id_inexistente_nao_modifica_a_base`; `test_rejeitar_identificadores_invalidos`; `test_excluir_nao_reutiliza_identificador` |

## Qualidade e interface

| RNF | Backlog | Evidência e limite |
|---|---|---|
| RNF01 | BL02, BL04, BL06 | `test_persistir_entre_instancias` e `test_ciclo_completo_persiste_entre_processos` verificam armazenamento e reabertura. |
| RNF02 | BL06 | CI configurada para Windows/Linux em Python 3.11/3.12. Verificação local feita em Linux/Python 3.12; demais ambientes dependem da execução remota. |
| RNF03 | BL03–BL06 | Testes CLI de entrada inválida, ID inexistente/não positivo/não numérico, filtro inválido, ajuda/versão e caminho inacessível verificam mensagens e códigos. |
| RNF04 | BL02–BL06 | `test_texto_parecido_com_sql_permanece_como_titulo`, testes de IDs/títulos e preservação de registros. SQL usa parâmetros e transações no repositório. |
| RNF05 | BL01, BL06, BL07 | Módulos de interface e regras separados; 26 testes executados com um comando, sem pacotes adicionais. |
| RNF06 | BL06, BL07 | Inspeção: nenhuma chamada de rede na aplicação e `.gitignore` exclui dados, ambientes, segredos locais e temporários. Isso não equivale a criptografia do banco. |
| RNF07 | BL06, BL07 | Arquivo de CI entregue; aprovação dos jobs no GitHub ainda não disponível. |

Em `tests/test_cli.py`, o ciclo completo cobre cadastro, listagem, filtros, conclusão e exclusão em processos separados. Os métodos `test_excluir_sem_confirmacao_nao_remove` e `test_ausencia_de_confirmacao_nao_cria_banco` verificam especificamente a confirmação de RF04.

## Evidência local

- Ambiente usado: Linux, Python 3.12.
- Comando: `python -m unittest discover -s tests -v`.
- Resultado: **26 testes executados, sem falhas ou erros** — 17 testes de regras/persistência e 9 de CLI.
- Os testes criam seus próprios bancos temporários. Nenhuma base pessoal acompanha o repositório.
- O resultado comprova a verificação local deste pacote. Não é um resultado de build remoto nem uma afirmação de que todos os caminhos possíveis foram testados.

## Vínculos no GitHub

| Item local | Issue real | PR real |
|---|---|---|
| BL01 | Pendente de criação | Pendente de criação |
| BL02 | Pendente de criação | Pendente de criação |
| BL03 | Pendente de criação | Pendente de criação |
| BL04 | Pendente de criação | Pendente de criação |
| BL05 | Pendente de criação | Pendente de criação |
| BL06 | Pendente de criação | Pendente de criação |
| BL07 | Pendente de criação | Pendente de criação |

Os números reais devem substituir os estados pendentes depois da publicação. Os IDs RF, CU, US e BL permanecem estáveis. Não há histórico Git, Issues, PRs ou tag remota incluídos no pacote de arquivos.
