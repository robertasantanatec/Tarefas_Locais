# Documentação do Tarefas Locais

Versão de referência: **0.2.0**. Revisão: **07/11/2026**.

| Documento | Conteúdo |
|---|---|
| [Termo de abertura](project-charter.md) | Justificativa, objetivos, escopo e responsáveis. |
| [Requisitos](requisitos.md) | RF01–RF06 e RNF01–RNF12. |
| [Casos de uso](casos-de-uso.md) | Atores, fluxos e exceções. |
| [Histórias](user-stories.md) | Valor e critérios de aceite. |
| [Backlog](backlog.md) | BL e Issues reais. |
| [Arquitetura](arquitetura.md) | Módulos, SQLite e execução. |
| [Rastreabilidade](rastreabilidade.md) | Requisito → Issue → código → testes. |
| [Desempenho](desempenho.md) | Método, RNF e baseline medida. |
| [Contribuição](../CONTRIBUTING.md) | Git Flow, commits, testes e PR. |
| [Changelog](../CHANGELOG.md) | Alterações por versão. |

## Regra de sincronização

PR que altera um RF deve atualizar requisitos, caso de uso, história, backlog, matriz e testes na mesma revisão. Mudanças de configuração, comandos ou instalação atualizam README e arquitetura. Registrar versão/data neste índice e mudança no changelog. O autor confere os critérios e evidências antes de integrar; não marcar verificação pendente como concluída. Novos commits e PRs incluem a Issue real. Não reescrever commits/tag históricos da versão 0.1.0.
