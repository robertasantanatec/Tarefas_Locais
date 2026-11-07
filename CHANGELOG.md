# Changelog

## [0.2.0] — 2026-11-07

### Adicionado

- Edição de título (RF05) e reabertura (RF06), com persistência, validação e testes; Issues #12/#13.
- Configuração TAREFAS_BANCO/.env.example e eventos JSON; #18/#22.
- Cobertura com gate 85%, Ruff, pre-commit, Gitleaks, pip-audit e Dependabot; #14/#16/#17/#20.
- CONTRIBUTING, índice com regra de sincronização e baseline real de desempenho; #15/#19/#21.
- Dockerfile, Compose com volume SQLite e verificação automática; #23.

### Corrigido

- Badge automático da CI, evidências da versão inicial e mapeamento BL01–BL07 → Issues #1–#7; #1/#7, PR #11.
- Template de PR com referência real e critério de fechamento; #7.

## [0.1.0] — 2026-11-07

- Cadastro, listagem/filtros, conclusão e exclusão confirmada em CLI/SQLite (RF01–RF04).
- 26 testes, documentação de engenharia, rastreabilidade, licença MIT e CI Windows/Linux com Python 3.11/3.12.
- Integração inicial por PR #8 para develop e PR #9 para main, tag anotada v0.1.0. Ajustes de release reintegrados por PR #10.
