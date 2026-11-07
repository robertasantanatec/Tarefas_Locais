# Requisitos

## Requisitos funcionais

### [RF01] Cadastrar tarefa

O sistema deve permitir cadastrar um título textual, atribuir um ID inteiro positivo e não reutilizado após exclusão e iniciar a tarefa como pendente.

- Espaços nas extremidades são removidos; sequências de espaços, tabulações e quebras de linha são convertidas em um espaço.
- Após essa normalização, o título deve ter de 1 a 120 caracteres e conter somente caracteres imprimíveis.
- Títulos inválidos não geram registros. Títulos iguais são permitidos, pois podem representar tarefas diferentes.
- Comando: `python -m src adicionar "Estudar requisitos"`.

### [RF02] Listar e filtrar tarefas

O sistema deve listar ID, situação e título em ordem crescente de ID. Deve aceitar os filtros `todas`, `pendentes` e `concluidas`, utilizando `todas` por padrão. Se não houver registros compatíveis, deve informar que nenhuma tarefa foi encontrada. Filtros desconhecidos devem ser rejeitados.

- Comando: `python -m src listar --status pendentes`.

### [RF03] Concluir tarefa

O sistema deve marcar como concluída a tarefa de ID informado, preservando os demais registros. O ID deve ser um inteiro maior que zero. ID inexistente deve produzir erro legível. Concluir novamente uma tarefa concluída deve informar a situação e manter seu estado, sem criar registros.

- Comando: `python -m src concluir 1`.

### [RF04] Excluir tarefa com confirmação

O sistema deve excluir permanentemente uma tarefa pendente ou concluída somente quando o usuário informar um ID válido e a opção `--confirmar`. Sem confirmação, nenhuma tarefa deve ser removida. ID inválido ou inexistente deve gerar mensagem de erro e preservar os registros existentes. O ID excluído não deve ser reaproveitado em cadastros posteriores.

- Comando: `python -m src excluir 1 --confirmar`.

### [RF05] Editar título

Comando `python -m src editar 1 "Novo título"`. Aplicar a mesma validação de RF01, preservar ID e situação e atualizar somente a tarefa escolhida. ID inválido ou inexistente e título inválido retornam erro sem alterar registros. A edição deve persistir em nova execução.

### [RF06] Reabrir tarefa

Comando `python -m src reabrir 1`. Alterar concluída para pendente preservando ID e título. Repetir em tarefa pendente informa a situação com sucesso e não cria registros. ID inválido ou inexistente retorna erro e preserva os registros.

## Requisitos não funcionais

| ID | Requisito verificável | Verificação |
|---|---|---|
| RNF01 | Persistir as alterações bem-sucedidas em SQLite e recuperá-las em uma nova execução com o mesmo banco. | Testes de reabertura e ciclo completo entre processos. |
| RNF02 | Executar com Python 3.11 ou superior com a dependência declarada em `requirements.txt`; os comandos devem ser compatíveis com Windows e Linux. | Matriz de CI em Python 3.11/3.12 nos dois sistemas. A matriz remota foi aprovada na [CI da versão 0.1.0](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648). |
| RNF03 | Disponibilizar ajuda e mensagens de negócio em português; retornar código 0 no sucesso, 1 em falha de negócio/acesso ao banco e 2 em erro de sintaxe de comando. Erros previstos não devem apresentar traceback. | Testes de CLI, `--help`, entradas inválidas e caminho de banco inacessível. A sintaxe de ajuda automática é fornecida pelo argparse. |
| RNF04 | Usar parâmetros nas consultas SQL, transações nas alterações e validações de título, ID e situação. | Testes de entrada semelhante a SQL, entradas inválidas e preservação dos demais registros. Restrições também definidas na tabela. |
| RNF05 | Separar interface e regras/persistência em módulos; manter uma suíte executável com um único comando após instalar `requirements-dev.txt`. | Inspeção de `src/` e execução de `python -m unittest discover -s tests -v`. |
| RNF06 | Manter o banco no computador do usuário, sem envio por rede, e excluir dados locais, ambientes e temporários do versionamento. | Inspeção do código e das regras de `.gitignore`. Sem autenticação ou criptografia nesta versão. |
| RNF07 | Automatizar os testes em pushes de branches de trabalho e em PRs para `develop` e `main`. | Workflow `.github/workflows/testes.yml`; aprovação remota verificada na [execução da versão 0.1.0](https://github.com/robertasantanatec/Tarefas_Locais/actions/runs/42376564648). |

### Qualidade e operação da versão 0.2.0

- **RNF08 — Desempenho:** p95 inferior a 1.000 ms por fluxo medido, com 1.000 tarefas iniciais e 30 repetições em máquina local ociosa. Fluxos e ambiente em [desempenho.md](desempenho.md). Limite do projeto para resposta interativa, não fornecido pelo professor. O benchmark retorna erro se excedido; não é garantia para qualquer hardware.
- **RNF09 — Qualidade:** Ruff lint e format aprovados; pre-commit com as mesmas regras. Cobertura de linhas e ramos em `src/` de pelo menos 85%, incluindo subprocessos. Limite inicial do projeto, abaixo da baseline de 99%, para impedir regressões relevantes. CI falha abaixo dele.
- **RNF10 — Diagnóstico:** eventos JSON em stderr com timestamp UTC, nível, evento, comando e ID quando aplicável; em erros previstos, incluir tipo da exceção. Títulos e caminhos não entram no evento JSON. Mensagens legíveis continuam separadas do evento, sem traceback.
- **RNF11 — Execução reprodutível:** Dockerfile e Compose executam a CLI e preservam SQLite em volume nomeado; CI verifica build, execução e persistência.
- **RNF12 — Segurança de entrega:** CI executa Gitleaks e pip-audit, falhando em achados; Dependabot verifica pip e Actions semanalmente. Não versionar `.env`, bancos e credenciais.

## Regras de domínio e limites

- Estados possíveis: pendente (`concluida = 0`) e concluída (`concluida = 1`). Transições: pendente → concluída e concluída → pendente.
- A exclusão pode ocorrer em qualquer estado e não possui desfazer.
- A normalização do título ocorre antes de medir seu tamanho.
- O banco padrão é `data/tarefas.sqlite3`, relativo ao diretório de execução. Precedência: `--banco` > `TAREFAS_BANCO` no ambiente > `.env` na raiz do projeto > padrão. Valor configurado vazio é rejeitado.
- O banco e sua tabela são criados no primeiro comando que os utilizar. Ajuda, versão e exclusão sem confirmação não precisam criar o banco.
- RF05 e RF06 ampliam o escopo na versão 0.2.0; a versão 0.1.0 original permanece identificada por sua tag. Autenticação e uso compartilhado continuam fora do escopo.

## Rastreabilidade

As associações de RFs e RNFs com histórias, casos de uso, backlog e testes estão em [rastreabilidade.md](rastreabilidade.md).
