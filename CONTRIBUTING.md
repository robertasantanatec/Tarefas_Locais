# Contribuição

## Ambiente

Use Python 3.11+, Git e SQLite. Clone o repositório, entre na raiz, crie `python -m venv .venv` e ative o ambiente (`source .venv/bin/activate` no Linux ou `.venv\Scripts\activate.bat` no Windows/Prompt). Execute:

```bash
python -m pip install -r requirements-dev.txt
python -m pre_commit install
```

Copie `.env.example` para `.env` se quiser configurar o banco. Nunca inclua dados pessoais ou credenciais em commits.

## Git Flow e commits

1. Abra ou reutilize uma Issue com objetivo, RF/RNF e critérios. Atribua responsável e rótulos.
2. Atualize `develop` e crie `feature/descricao`, `docs/descricao` ou `chore/descricao` para uma mudança coesa.
3. Separe mudanças independentes. Inclua código e testes relacionados; evite commits artificiais apenas para elevar contagem.
4. Use `feat: editar titulo (#12)`, `test: cobrir reabertura (#13)` ou `docs: atualizar matriz (#1)`; cada novo commit referencia a Issue real.
5. Execute as verificações abaixo e atualize os documentos afetados conforme [regra de sincronização](docs/README.md).
6. Abra PR para `develop`, com problema, alteração, RF/RNF, `Refs #N` ou `Closes #N` e evidência. `Closes` encerra automaticamente ao alcançar `main`, branch padrão. Confira o encerramento após a release.
7. Registre revisão individual dos critérios e aguarde todos os checks aprovados. Não declare revisão de outra pessoa.

`release/x.y.z` sai de `develop`, atualiza versão/changelog/badges e segue por PR para `main`; reintegre em `develop`. Use merge commit para preservar o histórico do Git Flow. Crie tag da nova versão após a CI verde em `main`, sem alterar tags publicadas. `hotfix/x.y.z` parte de `main` e retorna a `main` e `develop`.

## Verificações antes do PR

```bash
python -m ruff check .
python -m ruff format --check .
python -m pre_commit run --all-files
python -m coverage erase
python -m coverage run -m unittest discover -s tests -v
python -m coverage combine
python -m coverage report --fail-under=85
python -m pip_audit -r requirements-dev.txt
python tools/benchmark.py
```

O hook bloqueia violações de lint/formatação. Para formatar, use `python -m ruff format .`, revise o diff e repita os checks. A CI também verifica Gitleaks e Docker. Não ignorar falhas para concluir o PR.

## SemVer

Novas funcionalidades compatíveis da fase inicial levam 0.1.0 a 0.2.0. Correções compatíveis incrementam PATCH. Atualize `src/__init__.py`, teste de versão, README, índice, badge e changelog juntos. Após 1.0.0, mudanças incompatíveis incrementam MAJOR.
