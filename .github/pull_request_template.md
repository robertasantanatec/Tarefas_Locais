## Alteração

Descreva a mudança e o motivo.

## Rastreabilidade

- Issue no GitHub:
- ID local do backlog:
- RF / RNF / caso de uso / história:

Para encerrar uma Issue automaticamente, use `Closes #numero` substituindo `numero`
pelo número real da Issue. O fechamento automático ocorre quando a alteração chega
à branch padrão. Em PRs para develop, mantenha também o vínculo explícito.

## Verificação

- [ ] Os critérios de aceite foram conferidos.
- [ ] `python -m unittest discover -s tests -v` passou.
- [ ] Os documentos afetados foram atualizados.
- [ ] Os commits contêm mudanças relacionadas ao objetivo deste PR.
