# Baseline de desempenho — 0.2.0

Medição em 07/11/2026. Python 3.12.14, Linux-6.18.57-x86_64-with-glibc2.41.
SHA-256 de nomes/conteúdo de `src/*.py`, em ordem: `7c2192c76f5f2613ae9f81ceae2dbe69d891322c86b40534efe1cc0cba7b1c09`.

## Método e RNF08

Executar na raiz com o ambiente instalado:

```bash
python tools/benchmark.py
```

Banco temporário criado com 1.000 tarefas; um aquecimento por fluxo e 30 amostras com `perf_counter`. Mediana e p95 por nearest rank. O cadastro acrescenta 31 tarefas antes da listagem, portanto a listagem mede 1.031 registros. A CLI inclui abertura de processo e descarte de stdout/stderr; outros fluxos medem repositório/SQLite. Pares concluir/reabrir e adicionar/excluir incluem as duas operações. Nenhum dado pessoal é utilizado.

RNF08: p95 inferior a 1.000 ms por fluxo neste cenário, limite definido no projeto para resposta interativa. O script retorna 1 se algum fluxo ultrapassar o limite. Não é teste de concorrência nem garantia de tempo em qualquer computador; repetir no ambiente de destino.

| Fluxo | Mediana (ms) | p95 (ms) | RNF08 |
|---|---:|---:|---|
| adicionar | 0.102 | 0.437 | Atende |
| listar_1000 | 0.963 | 1.336 | Atende |
| editar | 0.079 | 0.125 | Atende |
| concluir_reabrir | 0.174 | 0.33 | Atende |
| adicionar_excluir | 0.181 | 0.281 | Atende |
| cli_listar | 66.045 | 73.515 | Atende |

## Qualidade e limites da verificação

34 testes locais aprovados em Python 3.12/Linux. Cobertura de linhas e ramos: 99% em `src/`, incluindo subprocessos; uma saída de ramo defensivo da CLI não percorrida. Gate: 85%, escolhido abaixo da baseline medida. Foi verificado que `coverage report --fail-under=100` retorna 2 e que pre-commit rejeita um arquivo temporário com import não utilizado/formatação inválida. Ruff aprovado; pip-audit não encontrou vulnerabilidades conhecidas nas dependências declaradas em 07/11/2026. Esses resultados são locais; os checks de cada PR ficam no GitHub. Docker e a matriz Windows/Linux devem ser confirmados pela CI, não por esta medição.
