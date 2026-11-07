# Backlog de engenharia

Os identificadores BL01–BL07 são locais e estáveis. Eles não representam números de Issues do GitHub. Cada item abaixo corresponde ao conteúdo de uma Issue; após sua criação, o número e o endereço reais devem ser registrados na tabela de rastreabilidade.

Prioridades: P1 = necessário ao produto/documentação; P2 = necessário ao fechamento da versão. A ordem considera dependências. O estado abaixo descreve o pacote local, sem presumir execução de PRs, CI ou releases no GitHub.

| Item | Prioridade | Dependências | Estado local |
|---|---|---|---|
| BL01 | P1 | — | Documentação produzida. |
| BL02 | P1 | BL01 | Cadastro implementado e testado. |
| BL03 | P1 | BL02 | Consulta e filtros implementados e testados. |
| BL04 | P1 | BL02, BL03 | Conclusão implementada e testada. |
| BL05 | P1 | BL02, BL03 | Exclusão implementada e testada. |
| BL06 | P1 | BL02–BL05 | 26 testes locais aprovados; CI configurada, execução remota pendente. |
| BL07 | P2 | BL01–BL06 | Versão e documentação preparadas; integração e tag remotas pendentes. |

## [BL01] Especificar o produto e seus critérios de aceite

**Objetivo:** definir o escopo da semana e as regras antes de organizar a implementação.  
**Rastreabilidade:** OBJ01; RF01–RF04; RNF01–RNF07; CU01–CU04; US01–US04.  
**Entregáveis:** charter, requisitos, casos de uso, histórias, arquitetura, backlog e matriz de rastreabilidade.

**Critérios de aceite:**

- [ ] O charter apresenta justificativa, objetivos mensuráveis, prazo, stakeholders e escopo dentro/fora da semana.
- [ ] Cada RF possui ID, caso de uso, história e critérios de aceite relacionados.
- [ ] Casos de uso apresentam fluxos principais, alternativos e de exceção.

## [BL02] Implementar cadastro de tarefa

**Objetivo:** persistir uma tarefa pendente com ID próprio.  
**Rastreabilidade:** RF01; RNF01, RNF04; CU01; US01.  
**Entregáveis:** comando `adicionar`, regra de título e inserção SQLite em `src/`; testes de cadastro em `tests/`.

**Critérios de aceite:**

- [ ] Título válido gera ID positivo e situação pendente.
- [ ] Espaços são normalizados; títulos de 1 e 120 caracteres são aceitos.
- [ ] Título vazio, longo ou não imprimível é rejeitado sem criar tarefa.
- [ ] O cadastro pode ser consultado em outra execução.

## [BL03] Implementar consulta com filtros

**Objetivo:** permitir acompanhar tarefas e pendências.  
**Rastreabilidade:** RF02; RNF03; CU02; US02.  
**Entregáveis:** comando `listar` e filtros; testes de ordenação e seleção de situação.

**Critérios de aceite:**

- [ ] A listagem exibe ID, situação e título em ordem crescente de ID.
- [ ] Os filtros `todas`, `pendentes` e `concluidas` apresentam os registros correspondentes.
- [ ] Base ou filtro sem resultados apresenta mensagem apropriada com sucesso.
- [ ] Filtro desconhecido é rejeitado pela CLI com código 2.

## [BL04] Implementar conclusão de tarefa

**Objetivo:** registrar o trabalho realizado sem afetar outras tarefas.  
**Rastreabilidade:** RF03; RNF01, RNF03, RNF04; CU03; US03.  
**Entregáveis:** comando `concluir`, atualização SQLite e testes de conclusão.

**Critérios de aceite:**

- [ ] Somente a tarefa escolhida é concluída e sua alteração persiste.
- [ ] Repetir uma conclusão mantém os registros e retorna mensagem de tarefa já concluída.
- [ ] ID inexistente, zero, negativo e não numérico seguem as respostas especificadas, sem alterar outros registros.

## [BL05] Implementar exclusão confirmada

**Objetivo:** remover um registro somente após confirmação explícita.  
**Rastreabilidade:** RF04; RNF03, RNF04; CU04; US04.  
**Entregáveis:** comando `excluir`, opção `--confirmar` e testes de preservação das demais tarefas.

**Critérios de aceite:**

- [ ] A exclusão com confirmação remove somente a tarefa indicada.
- [ ] Sem confirmação, a tarefa permanece e a CLI retorna código 1.
- [ ] IDs inválidos ou inexistentes são rejeitados; IDs excluídos não são reutilizados.

## [BL06] Verificar qualidade e automatizar testes

**Objetivo:** prevenir regressões e verificar regras em execuções independentes.  
**Rastreabilidade:** RNF01–RNF07; RF01–RF04; US01–US04.  
**Entregáveis:** `tests/test_tarefas.py`, `tests/test_cli.py` e workflow `testes.yml`.

**Critérios de aceite:**

- [ ] Os 26 testes passam com `python -m unittest discover -s tests -v`.
- [ ] A suíte verifica persistência entre processos, SQL parametrizado, erros legíveis e confirmação de exclusão.
- [ ] O workflow executa a suíte em Python 3.11/3.12 em Windows e Linux.
- [ ] As quatro combinações da CI passam no GitHub após a publicação. Esta evidência remota está pendente no pacote local.

## [BL07] Preparar e integrar a versão 0.1.0

**Objetivo:** entregar uma versão reproduzível com documentação sincronizada.  
**Rastreabilidade:** OBJ04; RNF05, RNF07; BL01–BL06.  
**Entregáveis:** README, licença MIT, changelog, badges, templates de Issue/PR e registros de integração no GitHub.

**Critérios de aceite:**

- [ ] O README diferencia funcionalidades implementadas e futuras, explica instalação/execução/testes e liga todos os documentos.
- [ ] A versão do código, README e changelog é 0.1.0.
- [ ] O histórico registra commits coesos e PRs vinculados às Issues reais.
- [ ] A release é integrada em `main` e `develop`, com testes aprovados e tag `v0.1.0` em `main`.

## Critério de pronto

Uma Issue só é encerrada após verificar seus critérios, revisar as mudanças, aprovar os testes aplicáveis e atualizar os documentos afetados. Preparar arquivos localmente não comprova a criação da Issue, a revisão do PR ou a aprovação da CI.
