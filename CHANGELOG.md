# Changelog

## Não lançado

### Corrigido

- Sincronização dos estados de versão e CI com as evidências do GitHub.
- Vínculos reais de BL01–BL07 às Issues e aos PRs.
- Reintegração dos ajustes finais da release em develop pelo PR #10.

## 0.1.0 — publicada

### Adicionado

- Cadastro de tarefas com validação de título, normalização de espaços e ID automático.
- Listagem em ordem de ID e filtros por situação.
- Conclusão idempotente e exclusão com confirmação explícita.
- Persistência local em SQLite e mensagens para erros previstos.
- 26 testes automatizados e configuração de CI para Windows/Linux em Python 3.11/3.12.
- Documentação de planejamento, backlog, rastreabilidade e política Git Flow.

Implementação pelo [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8), integração em main pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) e tag anotada `v0.1.0`. A [CI da versão](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648) aprovou os 26 testes iniciais em Windows/Linux e Python 3.11/3.12.
