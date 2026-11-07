# Casos de uso

## Atores e convenções

**Usuário:** pessoa que executa os comandos no terminal para gerenciar suas próprias tarefas. É o ator principal dos quatro casos. SQLite é um componente interno de persistência, não um ator externo.

Premissas comuns: executar a partir da raiz do projeto, com Python 3.11 ou superior e acesso de leitura/escrita ao caminho escolhido para o banco. As operações bem-sucedidas retornam código 0. Exceções previstas de negócio ou acesso ao banco retornam 1; erros de sintaxe tratados pelo parser retornam 2.

## [CU01] Cadastrar tarefa

**Ator:** Usuário. **Requisito:** RF01. **História:** US01.  
**Objetivo:** registrar uma tarefa que precisa ser realizada.  
**Pré-condição:** informar um título ao comando `adicionar`.  
**Pós-condição de sucesso:** um único registro pendente é persistido com ID próprio.

### Fluxo principal

1. O usuário executa `python -m src adicionar "Revisar conteúdo"`.
2. O sistema normaliza os espaços e valida o título.
3. O sistema grava a tarefa com ID automático e situação pendente.
4. O sistema informa o ID, o título e a situação inicial.

### Fluxos alternativos

- A1 — Título com espaços extras: no passo 2, o sistema os normaliza e continua o cadastro.
- A2 — Título igual ao de outra tarefa: o cadastro é aceito e recebe outro ID.

### Fluxos de exceção

- E1 — Título vazio, maior que 120 caracteres após normalização ou com controle não imprimível: o sistema informa erro e não cadastra.
- E2 — Ausência do argumento de título: o parser exibe o uso do comando e encerra com código 2.
- E3 — Erro de escrita/conexão: o sistema informa falha de acesso; o cadastro não é confirmado como concluído.

## [CU02] Consultar tarefas

**Ator:** Usuário. **Requisito:** RF02. **História:** US02.  
**Objetivo:** visualizar o trabalho registrado e suas situações.  
**Pré-condição:** escolher o comando `listar`.  
**Pós-condição de sucesso:** registros compatíveis são exibidos, sem alteração das tarefas existentes.

### Fluxo principal

1. O usuário executa `python -m src listar`.
2. O sistema consulta todas as tarefas em ordem crescente de ID.
3. O sistema exibe ID, situação e título de cada registro.

### Fluxos alternativos

- A1 — Filtro: o usuário informa `--status pendentes` ou `--status concluidas`; o sistema exibe somente as tarefas correspondentes.
- A2 — Nenhum resultado: o sistema informa `Nenhuma tarefa encontrada.` e retorna sucesso.
- A3 — Primeiro acesso sem banco: o sistema cria a estrutura vazia e aplica A2.

### Fluxos de exceção

- E1 — Filtro desconhecido: o parser rejeita o valor e encerra com código 2.
- E2 — Falha de leitura/criação do banco: o sistema informa o erro de acesso e encerra com código 1.

## [CU03] Concluir tarefa

**Ator:** Usuário. **Requisito:** RF03. **História:** US03.  
**Objetivo:** registrar que uma tarefa foi realizada.  
**Pré-condição de sucesso:** o ID corresponde a uma tarefa existente.  
**Pós-condição de sucesso:** a tarefa está concluída; as demais tarefas permanecem iguais.

### Fluxo principal

1. O usuário consulta os IDs disponíveis.
2. O usuário executa `python -m src concluir 1` para uma tarefa pendente.
3. O sistema valida o identificador e localiza o registro.
4. O sistema persiste a situação concluída e informa a conclusão.

### Fluxos alternativos

- A1 — Tarefa já concluída: o sistema informa que ela já estava concluída e retorna sucesso, preservando o estado e a quantidade de registros.

### Fluxos de exceção

- E1 — ID inexistente: o sistema informa que a tarefa não foi encontrada; os demais registros permanecem iguais.
- E2 — ID menor ou igual a zero: o sistema informa que o ID deve ser um inteiro maior que zero e retorna 1.
- E3 — ID ausente ou não numérico: o parser informa erro de uso e retorna 2.
- E4 — Falha de acesso: o sistema informa o erro e não confirma a conclusão.

## [CU04] Excluir tarefa

**Ator:** Usuário. **Requisito:** RF04. **História:** US04.  
**Objetivo:** remover definitivamente uma tarefa.  
**Pré-condições de sucesso:** tarefa existente e confirmação explícita no comando.  
**Pós-condição de sucesso:** somente a tarefa indicada foi removida; seu ID não será reutilizado.

### Fluxo principal

1. O usuário consulta os IDs e escolhe a tarefa.
2. O usuário executa `python -m src excluir 1 --confirmar`.
3. O sistema verifica a confirmação e valida o ID.
4. O sistema remove o registro e informa a exclusão.

### Fluxos alternativos

- A1 — Sem `--confirmar`: o sistema orienta a repetir o comando com confirmação, retorna 1 e não altera a base.
- A2 — Tarefa concluída: a exclusão segue o mesmo fluxo de uma tarefa pendente.

### Fluxos de exceção

- E1 — ID inexistente: o sistema informa que a tarefa não foi encontrada e preserva as demais.
- E2 — ID menor ou igual a zero, após confirmação: o sistema informa erro de validação e retorna 1.
- E3 — ID ausente ou não numérico: o parser retorna 2.
- E4 — Falha de acesso: o sistema informa o erro e não confirma a exclusão.
