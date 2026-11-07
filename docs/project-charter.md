# Termo de Abertura — Tarefas Locais

**Responsável:** Roberta Santana  
**Produto:** gerenciador pessoal de tarefas por terminal  
**Versão inicial:** 0.1.0  
**Duração prevista:** uma semana, organizada em sete dias de trabalho.

## Justificativa e visão do produto

Anotações dispersas dificultam identificar tarefas pendentes e acompanhar o que já foi concluído. O Tarefas Locais centraliza esse registro em uma aplicação pequena, executada no próprio computador. O usuário cadastra, consulta, conclui e exclui tarefas por comandos, com armazenamento permanente em SQLite.

O produto atende uma pessoa por instalação. A interface por terminal reduz o esforço de implementação e permite concentrar a semana nas regras do domínio, na documentação e na rastreabilidade do desenvolvimento.

## Objetivos SMART

| ID | Objetivo e prazo | Medida de conclusão |
|---|---|---|
| OBJ01 | Até o fim do dia 2, especificar as quatro operações centrais e os requisitos de qualidade. | Quatro RFs, casos de uso e histórias identificados e relacionados ao backlog. |
| OBJ02 | Até o fim do dia 4, disponibilizar cadastro, listagem com filtros, conclusão e exclusão confirmada. | Os cenários de aceite de US01 a US04 funcionam pela linha de comando. |
| OBJ03 | Até o fim do dia 5, verificar persistência, entradas inválidas e integridade das alterações. | Os 26 testes automatizados passam sem falhas em ambiente local; cada RF possui teste associado. |
| OBJ04 | Até o fim do dia 7, preparar a versão 0.1.0 e registrar seu fluxo de engenharia no GitHub. | Documentação sincronizada, Issues rastreáveis, PRs revisados, CI aprovada e tag v0.1.0 na main. A execução no GitHub depende da publicação do repositório. |

## Escopo da semana

Inclui:

- Cadastro de título com identificador automático e situação inicial pendente.
- Listagem por ID, com filtro de tarefas pendentes ou concluídas.
- Conclusão de tarefa existente e tratamento de conclusão repetida.
- Exclusão permanente somente com confirmação explícita.
- Persistência local em SQLite, validações e mensagens de erro.
- Documentação, backlog, testes, configuração de CI e política de branches e versões.

Fica fora do escopo desta semana:

- Interface gráfica, aplicação web, API e aplicativo móvel.
- Login, vários usuários, sincronização, nuvem e compartilhamento de tarefas.
- Edição de títulos, reabertura, prioridades, prazos, alertas e categorias.
- Criptografia do banco e rotinas automáticas de backup.

## Stakeholders e público-alvo

| Parte interessada | Papel e interesse |
|---|---|
| Roberta Santana | Responsável pela especificação, desenvolvimento, validação e manutenção do repositório. |
| Professor | Avalia consistência documental, implementação e uso do fluxo de versionamento. |
| Usuário individual familiarizado com terminal | Registra e acompanha tarefas pessoais em um computador, sem depender de conexão para usar a aplicação. |

## Plano da semana

| Período | Entrega prevista |
|---|---|
| Dias 1–2 | Charter, requisitos, casos de uso, histórias e backlog. |
| Dias 3–4 | Implementação das operações e armazenamento. |
| Dia 5 | Testes, correções e verificação dos critérios de aceite. |
| Dias 6–7 | Integração no GitHub, revisão, documentação final e versão 0.1.0. |

## Premissas, restrições e riscos

- Python 3.11 ou superior e terminal disponíveis; nenhum pacote adicional de execução é necessário.
- Os dados pertencem a uma instalação local. O diretório do banco precisa permitir escrita.
- O prazo é limitado a uma semana; funcionalidades futuras não entram na versão inicial.
- Erros de digitação são tratados por validações e ajuda de comandos. A exclusão exige a opção `--confirmar`.
- Perda do arquivo SQLite implica perda dos dados. O usuário pode copiar o arquivo, com a aplicação fechada, para manter um backup manual.
- A aplicação não se destina ao armazenamento de informações sensíveis: não oferece autenticação nem criptografia.

## Critério de encerramento

Os quatro requisitos funcionais devem estar implementados, os testes devem passar e todos os documentos devem corresponder ao comportamento entregue. O encerramento do fluxo no GitHub exige ainda Issues vinculadas aos PRs, integração em `main` e tag de versão. O pacote local contém os arquivos necessários; registros remotos só existirão após essas ações serem realizadas.
