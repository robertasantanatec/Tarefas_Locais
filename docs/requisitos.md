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

## Requisitos não funcionais

| ID | Requisito verificável | Verificação |
|---|---|---|
| RNF01 | Persistir as alterações bem-sucedidas em SQLite e recuperá-las em uma nova execução com o mesmo banco. | Testes de reabertura e ciclo completo entre processos. |
| RNF02 | Executar com Python 3.11 ou superior usando somente a biblioteca padrão; os comandos devem ser compatíveis com Windows e Linux. | Matriz de CI em Python 3.11/3.12 nos dois sistemas. O ambiente local foi verificado em Linux com Python 3.12; a matriz remota aguarda execução. |
| RNF03 | Disponibilizar ajuda e mensagens de negócio em português; retornar código 0 no sucesso, 1 em falha de negócio/acesso ao banco e 2 em erro de sintaxe de comando. Erros previstos não devem apresentar traceback. | Testes de CLI, `--help`, entradas inválidas e caminho de banco inacessível. A sintaxe de ajuda automática é fornecida pelo argparse. |
| RNF04 | Usar parâmetros nas consultas SQL, transações nas alterações e validações de título, ID e situação. | Testes de entrada semelhante a SQL, entradas inválidas e preservação dos demais registros. Restrições também definidas na tabela. |
| RNF05 | Separar interface e regras/persistência em módulos; manter uma suíte executável com um único comando e sem instalar bibliotecas externas. | Inspeção de `src/` e execução de `python -m unittest discover -s tests -v`. |
| RNF06 | Manter o banco no computador do usuário, sem envio por rede, e excluir dados locais, ambientes e temporários do versionamento. | Inspeção do código e das regras de `.gitignore`. Sem autenticação ou criptografia nesta versão. |
| RNF07 | Automatizar os testes em pushes de branches de trabalho e em PRs para `develop` e `main`. | Workflow `.github/workflows/testes.yml`; aprovação remota só pode ser verificada após publicar e executar a CI. |

## Regras de domínio e limites

- Estados possíveis: pendente (`concluida = 0`) e concluída (`concluida = 1`). Só existe a transição pendente → concluída.
- A exclusão pode ocorrer em qualquer estado e não possui desfazer.
- A normalização do título ocorre antes de medir seu tamanho.
- O banco padrão é `data/tarefas.sqlite3`, relativo ao diretório de execução. `--banco` permite selecionar outro arquivo.
- O banco e sua tabela são criados no primeiro comando que os utilizar. Ajuda, versão e exclusão sem confirmação não precisam criar o banco.
- O sistema não oferece edição, reabertura, autenticação ou uso compartilhado. Esses recursos não constituem critérios de aceite da versão 0.1.0.

## Rastreabilidade

As associações de RFs e RNFs com histórias, casos de uso, backlog e testes estão em [rastreabilidade.md](rastreabilidade.md).
