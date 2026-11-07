"""Eventos JSON em stderr; títulos e caminhos pessoais não são registrados."""

import json
import sys
from datetime import datetime, timezone


def registrar(
    nivel: str, evento: str, comando: str, tarefa_id: int | None = None, erro: str | None = None
) -> None:
    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": nivel,
        "event": evento,
        "command": comando,
    }
    if tarefa_id is not None:
        registro["task_id"] = tarefa_id
    if erro is not None:
        registro["error_type"] = erro
    print(json.dumps(registro, ensure_ascii=False), file=sys.stderr)
