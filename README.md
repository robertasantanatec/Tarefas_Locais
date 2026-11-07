# Tarefas Locais

![Versão 0.2.0](.github/badges/versao.svg)
![Licença MIT](.github/badges/licenca.svg)
[![Testes](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/testes.yml/badge.svg?branch=main)](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/testes.yml)
[![Segurança](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/seguranca.yml/badge.svg?branch=main)](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/seguranca.yml)
[![Docker](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/docker.yml/badge.svg?branch=main)](https://github.com/robertasantanatec/Tarefas_Locais/actions/workflows/docker.yml)

Gerenciador pessoal de tarefas por terminal, com persistência SQLite no computador do usuário. Centraliza pendências, conclusões e correções de descrição. Desenvolvido por **Roberta Santana**. Versão do código: **0.2.0**.

## Funcionalidades

| Estado | Recurso |
|---|---|
| Implementado — RF01 | Cadastrar título válido, normalizar espaços e gerar ID pendente. |
| Implementado — RF02 | Listar por ID e filtrar todas, pendentes ou concluídas. |
| Implementado — RF03 | Concluir tarefa, inclusive repetição idempotente. |
| Implementado — RF04 | Excluir somente com confirmação explícita. |
| Implementado — RF05 | Editar título preservando ID e situação. |
| Implementado — RF06 | Reabrir tarefa concluída sem duplicar registros. |
| Implementado | Configuração do banco, logs JSON, controles de qualidade e Docker. |
| Futuro, fora desta correção | Prazos, categorias e exportação; itens 16–25 do PDF. |

A tag `v0.1.0` preserva a entrega inicial, publicada pelo [PR #9](https://github.com/robertasantanatec/Tarefas_Locais/pull/9), com [26 testes aprovados na CI](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648). O [PR #10](https://github.com/robertasantanatec/Tarefas_Locais/pull/10) reintegrou os ajustes em `develop`, e o [PR #11](https://github.com/robertasantanatec/Tarefas_Locais/pull/11) sincronizou documentação e evidências. Os badges acima consultam o estado atual dos workflows em `main`.

## Instalação e execução local

Requisitos: Python 3.11+ com SQLite e terminal; Git para contribuir. A aplicação depende de `python-dotenv`, declarado em requirements.txt.

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/robertasantanatec/Tarefas_Locais.git
   cd Tarefas_Locais
   python -m venv .venv
   ```

2. Ative o ambiente. Linux: `source .venv/bin/activate`. Windows/Prompt: `.venv\Scripts\activate.bat`. Instale:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Para configurar o caminho, copie `.env.example` para `.env` na raiz (`cp .env.example .env` no Linux; `copy .env.example .env` no Windows). O exemplo já funciona com o banco padrão. Não publique `.env` ou dados pessoais.
4. Confira a ajuda e execute na raiz:

   ```bash
   python -m src --help
   python -m src --version
   python -m src adicionar "Estudar testes"
   python -m src listar
   python -m src listar --status pendentes
   python -m src editar 1 "Revisar testes"
   python -m src concluir 1
   python -m src reabrir 1
   python -m src excluir 1 --confirmar
   ```

Use o ID real exibido na listagem. Títulos devem ter entre 1 e 120 caracteres imprimíveis após normalizar espaços. Exclusão confirmada é permanente. Concluir tarefa já concluída ou reabrir tarefa já pendente retorna sucesso sem duplicar registros.

### Banco e configuração

| Opção | Descrição |
|---|---|
| `TAREFAS_BANCO` | Caminho SQLite. Padrão `data/tarefas.sqlite3`, relativo ao diretório de execução. |
| `--banco CAMINHO` | Opção global antes do subcomando; prevalece sobre a configuração. |

Precedência: `--banco` > variável do processo > `.env` na raiz do projeto > padrão. Valor configurado vazio é erro. Exemplo: `python -m src --banco data/exemplo.sqlite3 listar`. Banco/tabela são criados no primeiro comando que os usa. Ajuda, versão e exclusão sem confirmação não criam banco. Backup manual: feche a aplicação e copie o SQLite. Não há autenticação, criptografia ou sincronização.

### Saída e diagnóstico

Sucesso retorna 0; erro de negócio/acesso ao banco retorna 1; erro de sintaxe retorna 2. Resultados ficam em stdout. Eventos JSON vão para stderr com timestamp UTC, nível, comando, evento e ID quando conhecido. Erros incluem tipo da exceção; títulos e caminhos não são incluídos no evento JSON. Mensagens legíveis de falha também são escritas em stderr, em linha separada, sem traceback. Não tratar todo stderr como um único JSON.

## Testes e qualidade

```bash
python -m pip install -r requirements-dev.txt
python -m pre_commit install
python -m ruff check .
python -m ruff format --check .
python -m coverage erase
python -m coverage run -m unittest discover -s tests -v
python -m coverage combine
python -m coverage report --fail-under=85
python -m pip_audit -r requirements-dev.txt
python tools/benchmark.py
```

34 testes locais aprovados em Python 3.12/Linux, com bancos temporários. Cobertura medida: 99% de linhas/ramos em `src/`, incluindo subprocessos. O gate de 85% foi definido pelo projeto abaixo dessa baseline; a CI reprova resultados inferiores. Testes negativos confirmaram que o gate e os hooks rejeitam violações. [Método e desempenho medido](docs/desempenho.md).

A CI executa testes, cobertura, Ruff e formatação em Python 3.11/3.12 e Windows/Linux. Workflows adicionais executam Gitleaks, pip-audit e build/persistência Docker. Dependabot verifica pip e GitHub Actions semanalmente, propondo PRs para `develop`. Resultado local não substitui a aprovação dos checks do PR.

## Docker

Requisitos: Docker e plugin Compose. Na raiz:

```bash
docker compose up --build
docker compose run --rm tarefas adicionar "Tarefa no container"
docker compose run --rm tarefas listar
docker compose down
```

A aplicação é uma CLI: `up` executa a listagem e termina com código 0; não mantém servidor escutando. O volume `tarefas-data` mantém o SQLite entre containers. `down` preserva esse volume; `down --volumes` apaga os dados e deve ser usado apenas quando essa exclusão for intencional.

## Documentação

- [Índice e regra de sincronização](docs/README.md)
- [Termo de abertura](docs/project-charter.md)
- [Requisitos](docs/requisitos.md)
- [Casos de uso](docs/casos-de-uso.md)
- [Histórias e critérios de aceite](docs/user-stories.md)
- [Backlog](docs/backlog.md)
- [Arquitetura e dados](docs/arquitetura.md)
- [Rastreabilidade](docs/rastreabilidade.md)
- [Baseline de desempenho](docs/desempenho.md)
- [Contribuição](CONTRIBUTING.md), [changelog](CHANGELOG.md) e [licença MIT](LICENSE)

## Git Flow e SemVer

| Branch | Origem | Integração |
|---|---|---|
| `main` | Repositório | Recebe versões estáveis por PR; mesma URL da entrega. |
| `develop` | `main` | Recebe branches de trabalho e reintegrações. |
| `feature/*`, `docs/*`, `chore/*` | `develop` | PR revisado para `develop`, com Issue real e CI verde. |
| `release/x.y.z` | `develop` | PR para `main`, tag da versão após CI; reintegração em `develop`. |
| `hotfix/x.y.z` | `main` | PR para `main` e reintegração em `develop`. |

Commits coesos seguem Conventional Commits e citam Issue: `feat: editar titulo (#12)`. PRs referenciam critérios/testes e usam `Closes #N` quando completos; o fechamento automático ocorre ao alcançar `main`. Revisão individual é registrada sem atribuí-la a terceiros. O histórico antigo e tags publicadas são preservados.

SemVer `MAJOR.MINOR.PATCH`: 0.2.0 acrescenta edição/reabertura à entrega 0.1.0. Correções compatíveis incrementam PATCH; após 1.0.0, incompatibilidades incrementam MAJOR. Versão do código, teste, README, índice, badge e changelog são atualizados juntos. Veja [CONTRIBUTING](CONTRIBUTING.md).
