# Histórias de usuário

Os cenários abaixo são os critérios de aceite da versão 0.1.0. Cada cenário usa um banco conhecido e independente, evitando interferência de dados de outras execuções.

## [US01] Registrar tarefa — RF01 / CU01 / BL02

Como usuário, quero cadastrar uma tarefa para que eu possa registrar o que preciso fazer.

```gherkin
Cenário: Cadastrar com sucesso
  Dado que posso gravar no banco de tarefas
  Quando cadastro o título "Estudar Python"
  Então recebo um ID inteiro positivo
  E a tarefa é armazenada como pendente
  E posso consultá-la em uma nova execução

Cenário: Normalizar espaços
  Dado que informo o título "  Estudar   Python  "
  Quando realizo o cadastro
  Então o título armazenado é "Estudar Python"

Cenário: Validar os limites do título
  Dado que o tamanho é medido após normalizar os espaços
  Quando cadastro um título imprimível com 1 ou 120 caracteres
  Então o cadastro é aceito
  Quando tento cadastrar título vazio, somente espaços ou com 121 caracteres
  Então recebo erro de validação
  E nenhum novo registro é criado pela tentativa inválida

Cenário: Rejeitar controle não imprimível
  Dado que o título contém um caractere nulo
  Quando tento cadastrá-lo
  Então recebo erro de validação
  E o título não é armazenado
```

## [US02] Consultar tarefas — RF02 / CU02 / BL03

Como usuário, quero listar e filtrar minhas tarefas para que eu possa identificar pendências e consultar o que já concluí.

```gherkin
Cenário: Listar todas
  Dado que existem tarefas pendentes e concluídas
  Quando executo a listagem sem filtro
  Então vejo todas em ordem crescente de ID
  E cada linha informa ID, situação e título

Cenário: Filtrar por situação
  Dado que existem tarefas nas duas situações
  Quando listo com o filtro "pendentes"
  Então vejo somente tarefas pendentes
  Quando listo com o filtro "concluidas"
  Então vejo somente tarefas concluídas

Cenário: Nenhum resultado
  Dado que não há tarefas compatíveis com a consulta
  Quando realizo a listagem
  Então vejo "Nenhuma tarefa encontrada."
  E a operação retorna código 0

Cenário: Filtro inválido
  Dado que utilizo a interface de terminal
  Quando informo um filtro diferente de "todas", "pendentes" ou "concluidas"
  Então recebo erro de uso com código 2
  E nenhum registro existente é alterado
```

## [US03] Concluir tarefa — RF03 / CU03 / BL04

Como usuário, quero marcar uma tarefa como concluída para que eu possa acompanhar o trabalho realizado.

```gherkin
Cenário: Concluir tarefa pendente
  Dado que existem duas tarefas pendentes com IDs diferentes
  Quando concluo uma delas pelo ID
  Então somente a tarefa escolhida passa a concluída
  E a alteração permanece em uma nova execução

Cenário: Repetir uma conclusão
  Dado que a tarefa já está concluída
  Quando solicito sua conclusão novamente
  Então recebo uma mensagem de que ela já estava concluída
  E a operação retorna código 0
  E nenhum registro é criado ou removido

Cenário: ID inexistente
  Dado que o ID 999 não existe no banco utilizado
  Quando tento concluir a tarefa 999
  Então recebo mensagem de tarefa não encontrada e código 1
  E os registros existentes permanecem iguais

Cenário: ID inválido
  Dado que utilizo a interface de terminal
  Quando informo ID 0 ou negativo
  Então recebo erro de validação com código 1
  Quando informo um ID não numérico
  Então recebo erro de uso com código 2
```

## [US04] Remover tarefa — RF04 / CU04 / BL05

Como usuário, quero excluir uma tarefa com confirmação para que eu possa remover registros sem apagá-los por uma omissão acidental da confirmação.

```gherkin
Cenário: Exclusão confirmada
  Dado que existem duas tarefas com IDs diferentes
  Quando excluo uma delas com a opção "--confirmar"
  Então somente a tarefa escolhida é removida permanentemente
  E a outra tarefa permanece disponível
  E um novo cadastro não reutiliza o ID removido

Cenário: Exclusão sem confirmação
  Dado que a tarefa informada existe
  Quando executo a exclusão sem "--confirmar"
  Então sou orientado a confirmar a exclusão
  E recebo código 1
  E a tarefa permanece no banco

Cenário: ID inexistente
  Dado que o ID 999 não existe no banco utilizado
  Quando tento excluí-lo com confirmação
  Então recebo mensagem de tarefa não encontrada e código 1
  E os registros existentes permanecem iguais

Cenário: ID inválido
  Dado que confirmo a operação
  Quando informo ID 0 ou negativo
  Então recebo erro de validação com código 1
  Quando informo um ID não numérico
  Então recebo erro de uso com código 2
```

## Critérios transversais

- Erros previstos de acesso ao banco devem apresentar mensagem legível e código 1, sem traceback.
- `python -m src --help` deve apresentar os comandos disponíveis sem criar banco.
- Os testes devem usar diretórios temporários e não alterar o banco pessoal do usuário.
- A conclusão do fluxo de engenharia exige vínculos reais entre Issues, PRs e requisitos; esses vínculos serão registrados após a publicação no GitHub.
