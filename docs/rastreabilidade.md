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
| RNF02 | BL06 | CI configurada para Windows/Linux em Python 3.11/3.12. Verificação local em Linux/Python 3.12 e [matriz remota aprovada](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648). |
| RNF03 | BL03–BL06 | Testes CLI de entrada inválida, ID inexistente/não positivo/não numérico, filtro inválido, ajuda/versão e caminho inacessível verificam mensagens e códigos. |
| RNF04 | BL02–BL06 | `test_texto_parecido_com_sql_permanece_como_titulo`, testes de IDs/títulos e preservação de registros. SQL usa parâmetros e transações no repositório. |
| RNF05 | BL01, BL06, BL07 | Módulos de interface e regras separados; 26 testes executados com um comando, sem pacotes adicionais. |
| RNF06 | BL06, BL07 | Inspeção: nenhuma chamada de rede na aplicação e `.gitignore` exclui dados, ambientes, segredos locais e temporários. Isso não equivale a criptografia do banco. |
| RNF07 | BL06, BL07 | [Workflow executado e aprovado na main da versão 0.1.0](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648). |

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
| BL01 | [#1](https://github.com/robertasantanatec/Tarefas_Locais/issues/1) | [Commit inicial b0e1183](https://github.com/robertasantanatec/Tarefas_Locais/commit/b0e11835398bdc65b31ea083bb76422fec6c686b); não houve PR da base documental |
| BL02 | [#2](https://github.com/robertasantanatec/Tarefas_Locais/issues/2) | [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8), integrado pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) |
| BL03 | [#3](https://github.com/robertasantanatec/Tarefas_Locais/issues/3) | [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8), integrado pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) |
| BL04 | [#4](https://github.com/robertasantanatec/Tarefas_Locais/issues/4) | [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8), integrado pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) |
| BL05 | [#5](https://github.com/robertasantanatec/Tarefas_Locais/issues/5) | [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8), integrado pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) |
| BL06 | [#6](https://github.com/robertasantanatec/Tarefas_Locais/issues/6) | [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8), integrado pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) |
| BL07 | [#7](https://github.com/robertasantanatec/Tarefas_Locais/issues/7) | [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) e [PR #10](https://github.com/robertasantanatec/Tarefas_Locais/pull/10) |

Os IDs RF, CU, US e BL permanecem estáveis e são complementados pelos números reais do GitHub. A tag anotada [v0.1.0](https://github.com/robertasantanatec/Tarefas_Locais/releases/tag/v0.1.0) identifica a versão inicial. A [CI da main](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648) registrou a aprovação das quatro combinações. Os vínculos acima permitem consultar as evidências no repositório.

## Evolução 0.2.0 — avaliação Week_01

| Item | Issue real | Implementação / verificação |
|---|---|---|
| RF05 / CU05 / US05 / BL08 | [#12](https://github.com/robertasantanatec/Tarefas_Locais/issues/12) | `RepositorioTarefas.editar`, CLI `editar`; `test_editar_preserva_id_estado_e_outros_registros`, `test_editar_rejeita_invalidos_sem_alterar_registros`, `test_editar_limites_e_sql_parametrizado`, `test_ciclo_completo_persiste_entre_processos`. |
| RF06 / CU06 / US06 / BL09 | [#13](https://github.com/robertasantanatec/Tarefas_Locais/issues/13) | `RepositorioTarefas.reabrir`, CLI `reabrir`; `test_reabrir_persiste_sem_afetar_outros`, `test_reabrir_invalido_e_inexistente_preserva_dados`, ciclo entre processos. |
| QA-COV / RNF09 | [#14](https://github.com/robertasantanatec/Tarefas_Locais/issues/14) | `.coveragerc`, testes.yml; baseline local 99%, gate 85%. |
| DOC-CTB | [#15](https://github.com/robertasantanatec/Tarefas_Locais/issues/15) | CONTRIBUTING.md. |
| SEC-SCAN / RNF12 | [#16](https://github.com/robertasantanatec/Tarefas_Locais/issues/16) | seguranca.yml: Gitleaks + pip-audit. |
| DEP-BOT / RNF12 | [#17](https://github.com/robertasantanatec/Tarefas_Locais/issues/17) | dependabot.yml semanal, pip/Actions. |
| ENV-EX | [#18](https://github.com/robertasantanatec/Tarefas_Locais/issues/18) | config.py, .env.example; `test_configuracao_precedencia_env_e_exemplo`. |
| DOC-IDX | [#19](https://github.com/robertasantanatec/Tarefas_Locais/issues/19) | docs/README.md, versão/data/regra de sincronização. |
| QA-LINT / RNF09 | [#20](https://github.com/robertasantanatec/Tarefas_Locais/issues/20) | Ruff, pre-commit e CI; teste negativo de hook em repositório temporário. |
| PERF-BASE / RNF08 | [#21](https://github.com/robertasantanatec/Tarefas_Locais/issues/21) | tools/benchmark.py e desempenho.md, medições reais. |
| OBS-LOG / RNF10 | [#22](https://github.com/robertasantanatec/Tarefas_Locais/issues/22) | observabilidade.py; `test_logs_de_erro_tem_identificador_e_contexto` e `test_cli_editar_reabrir_e_logs_json_sem_titulo`. |
| DOCK-01 / RNF11 | [#23](https://github.com/robertasantanatec/Tarefas_Locais/issues/23) | Dockerfile, docker-compose.yml e docker.yml com persistência entre containers. |

DOC-SYNC/TRC-ISS reutilizam #1 e #7, com [PR #11](https://github.com/robertasantanatec/Tarefas_Locais/pull/11). GIT-ISS reutiliza #7 para template, referências e verificação de integração/encerramento. Números do PDF são ordens da avaliação; #12–#23 são os números efetivamente atribuídos pelo GitHub.
