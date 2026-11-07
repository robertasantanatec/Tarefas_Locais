# Tarefas Locais

![Versão 0.1.0](.github/badges/versao.svg)
![Licença MIT](.github/badges/licenca.svg)
![Testes locais: 26 aprovados](.github/badges/testes.svg)
[![Testes](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/testes.yml/badge.svg?branch=main)](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/testes.yml)

Gerenciador pessoal de tarefas por terminal, com dados armazenados em SQLite. Permite registrar pendências e acompanhar conclusões sem manter anotações dispersas. Desenvolvido por **Roberta Santana**.

## Funcionalidades

| Situação | Funcionalidade |
|---|---|
| Implementada — RF01 | Cadastrar título válido, normalizar espaços e gerar ID com situação pendente. |
| Implementada — RF02 | Listar tarefas por ID e filtrar todas, pendentes ou concluídas. |
| Implementada — RF03 | Concluir tarefa e tratar conclusão repetida sem duplicação. |
| Implementada — RF04 | Excluir tarefa somente com confirmação explícita. |
| Implementada | Persistir dados entre execuções e apresentar erros previstos sem traceback. |
| Planejada para depois da semana | Edição de título e reabertura de tarefa; dependem de nova especificação e versão. |

A versão publicada é **0.1.0**, integrada em `main` pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) e identificada pela tag anotada `v0.1.0`. A [CI da versão 0.1.0](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648) aprovou os 26 testes nas quatro combinações de Windows/Linux e Python 3.11/3.12. Os ajustes finais da release foram reintegrados em `develop` pelo [PR #10](https://github.com/robertasantanatec/Tarefas_Locais/pull/10). O badge de testes consulta o estado atual do Actions.

## Ambiente e instalação

Requisitos: **Python 3.11 ou superior** com suporte a SQLite e um terminal. Git é necessário para versionar/publicar, mas não para executar a aplicação. Não há bibliotecas de terceiros nem etapa de `pip install`.

1. Clone o repositório e abra um terminal na raiz da pasta `Tarefas_Locais`.
2. Verifique o Python e o SQLite:

   ```bash
   python --version
   python -c "import sqlite3; print(sqlite3.sqlite_version)"
   ```

3. Opcionalmente, crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   Ative no Linux/macOS com `source .venv/bin/activate`. No Windows, usando Prompt de Comando, execute `.venv\Scripts\activate.bat`.

4. Consulte a ajuda e execute a aplicação:

   ```bash
   python -m src --help
   python -m src --version
   python -m src adicionar "Revisar requisitos"
   python -m src listar
   ```

Em ambientes nos quais o executável se chama `python3` ou `py`, substitua `python` pelo comando correspondente. Confirme que a versão atende ao requisito.

## Uso

Execute os comandos a partir da raiz do projeto:

```bash
python -m src adicionar "Estudar testes"
python -m src listar
python -m src listar --status pendentes
python -m src concluir 1
python -m src listar --status concluidas
python -m src excluir 1 --confirmar
```

O ID `1` é um exemplo: utilize o ID retornado pelo cadastro ou mostrado na listagem. O título deve ter de 1 a 120 caracteres após normalizar os espaços. Use aspas para títulos com espaços. Títulos iguais são aceitos com IDs diferentes.

Sem `--confirmar`, a exclusão é recusada. A exclusão confirmada é permanente. Uma tarefa já concluída pode ser concluída novamente sem alteração de estado.

### Banco de dados

O arquivo padrão é `data/tarefas.sqlite3`, criado automaticamente quando necessário. O caminho é relativo ao diretório de execução; mantenha a execução na raiz para usar sempre a mesma base. Não envie dados pessoais ao repositório.

Para escolher outra base, informe a opção global **antes do subcomando**:

```bash
python -m src --banco data/exemplo.sqlite3 adicionar "Preparar entrega"
python -m src --banco data/exemplo.sqlite3 listar
```

O arquivo precisa de permissão de leitura/escrita. Para backup manual, feche a aplicação e copie o arquivo SQLite. Não há login, sincronização, criptografia ou backup automático.

### Códigos de saída

| Código | Significado |
|---|---|
| 0 | Sucesso, incluindo consulta vazia, ajuda, versão e conclusão repetida. |
| 1 | Erro de validação/regra, falta de confirmação, tarefa inexistente ou falha de acesso ao banco. |
| 2 | Uso incorreto do comando, como argumento ausente, ID não numérico ou filtro desconhecido. |

## Testes e integração contínua

```bash
python -m unittest discover -s tests -v
```

São **26 testes**, com bancos temporários: 17 verificam regras/persistência e 9 verificam a CLI em processos separados. A execução local em Linux com Python 3.12 passou sem falhas. A suíte não utiliza o banco pessoal em `data/`.

O [workflow de testes](.github/workflows/testes.yml) executa a suíte em Python 3.11 e 3.12, em Windows e Linux, nos pushes previstos e em PRs para `develop` e `main`. A [execução remota da versão 0.1.0](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648) foi aprovada. As verificações da versão instalada devem ser repetidas antes de integrar novas alterações.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `docs/` | Planejamento, especificações, backlog, arquitetura e rastreabilidade. |
| `src/` | Código Python da aplicação. |
| `tests/` | Testes de domínio, persistência e terminal. |
| `.github/` | Workflow, templates de Issue/PR e badges. |
| `.gitignore` | Exclusão de dados locais, ambientes e temporários. |
| `CHANGELOG.md` | Mudanças da versão preparada. |
| `LICENSE` | Licença MIT. |

## Documentação


- [Termo de Abertura](docs/project-charter.md)
- [Requisitos funcionais e não funcionais](docs/requisitos.md)
- [Casos de uso](docs/casos-de-uso.md)
- [Histórias e critérios de aceite](docs/user-stories.md)
- [Backlog de engenharia](docs/backlog.md)
- [Arquitetura e modelo de dados](docs/arquitetura.md)
- [Rastreabilidade e validação](docs/rastreabilidade.md)
- [Changelog](CHANGELOG.md) e [licença](LICENSE)

## Fluxo de branches — Git Flow

| Branch | Origem | Finalidade | Integração |
|---|---|---|---|
| `main` | Inicialização do repositório | Versões estáveis e tags. | Recebe `release/*` e `hotfix/*` por PR. |
| `develop` | `main` | Integração da próxima versão. | Recebe `feature/*`, correções de release e hotfixes. |
| `feature/BLxx-descricao` | `develop` | Uma mudança coesa ligada ao backlog. | PR para `develop`, com testes e vínculos às Issues. |
| `release/0.1.0` | `develop` | Revisão, ajustes finais e documentação da versão. | PR para `main` e reintegração em `develop`. |
| `hotfix/0.1.1` | `main` | Correção urgente de versão publicada. | PR para `main` e reintegração em `develop`. |

O fluxo é aplicado no repositório: [PR #8](https://github.com/robertasantanatec/Tarefas_Locais/pull/8) integra a implementação em `develop`, [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9) publica a versão 0.1.0 em `main` e [PR #10](https://github.com/robertasantanatec/Tarefas_Locais/pull/10) reintegra os ajustes finais em `develop`. Cada mudança nova deve citar os IDs aplicáveis e a Issue real, por exemplo `RF01 / US01 / BL02 / #2`. O [backlog](docs/backlog.md) fornece o conteúdo das Issues e os [templates](.github/ISSUE_TEMPLATE/atividade.md) padronizam seu registro.

### Commits atômicos e revisão

Um commit deve conter uma alteração coesa com os testes correspondentes, sem misturar mudanças independentes. Exemplos de mensagens: `feat: cadastrar tarefa com persistência (#2)`, `fix: rejeitar título vazio (#2)` e `docs: detalhar fluxo de exclusão (#5)`.

Antes do PR, executar os testes e atualizar os documentos afetados. O [template de PR](.github/pull_request_template.md) inclui a rastreabilidade e a validação. Em trabalho individual, registrar a própria revisão dos critérios e dos testes. Não declarar uma revisão de outra pessoa que não ocorreu. O fechamento automático de Issues por palavras como `Closes #N` depende de a alteração alcançar a branch padrão do repositório.

### Versionamento semântico

Usar `MAJOR.MINOR.PATCH`. O produto está em desenvolvimento inicial, versão `0.1.0`: correções compatíveis seguem como `0.1.1`; novas funcionalidades previstas seguem como `0.2.0`. Até `1.0.0`, registrar explicitamente mudanças incompatíveis, pois a interface ainda não é estável. Após `1.0.0`, incompatibilidades exigem incremento de MAJOR. Atualizar `src/__init__.py`, changelog e badge de versão em conjunto. A tag `v0.1.0` identifica o commit publicado da versão inicial. Para versões seguintes, criar uma nova tag apenas no commit aprovado e integrado em `main`, preservando as tags já publicadas.
