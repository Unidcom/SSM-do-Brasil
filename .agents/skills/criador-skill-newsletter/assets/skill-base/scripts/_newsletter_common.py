"""Utilitários compartilhados pelos scripts da skill de newsletter.

Gerado por criador-skill-newsletter. Todos os scripts leem `config/newsletter.json`
da própria skill e resolvem a raiz do projeto subindo até encontrar `.git`, de modo
que funcionam independentemente do diretório atual.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_DIR / "config" / "newsletter.json"

# Mojibake (UTF-8 lido como Latin-1/cp1252) mostra "Ã"/"Â" seguido de outro caractere
# não-ASCII. Português legítimo ("REGULAÇÃO", "ÂNGULO") tem letra ASCII depois.
MOJIBAKE_RE = re.compile(r"[ÃÂ][^\x00-\x7F]")
EDITION_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:-[0-9a-z]+)?$")

# Formato interno do payload.json — igual para todas as plataformas. Os adaptadores
# de create_draft.py convertem para o corpo que cada API espera.
PAYLOAD_FIELDS = ("nome_campanha", "assunto", "pre_header", "html", "texto", "link_aprovacao")


class NewsletterError(RuntimeError):
    """Erro exibível ao operador, sem segredos."""


def project_root() -> Path:
    for candidate in [SKILL_DIR, *SKILL_DIR.parents]:
        if (candidate / ".git").exists():
            return candidate
    # .agents/skills/<skill> → raiz três níveis acima
    return SKILL_DIR.parents[2]


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        if default is not None:
            return default
        raise NewsletterError(f"Arquivo não encontrado: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise NewsletterError(f"JSON inválido em {path}: {exc}") from exc


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_config() -> dict[str, Any]:
    return read_json(CONFIG_PATH)


def today(config: dict[str, Any]) -> date:
    tz_name = config.get("fuso", "America/Sao_Paulo")
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo(tz_name)).date()
    except Exception:
        # Windows sem o pacote tzdata: Brasil não tem horário de verão desde 2019.
        if tz_name == "America/Sao_Paulo":
            return datetime.now(timezone(timedelta(hours=-3))).date()
        return date.today()


def parse_date(value: str | None, config: dict[str, Any]) -> date:
    if not value:
        return today(config)
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise NewsletterError(f"Data inválida (use AAAA-MM-DD): {value}") from exc


def editions_root(config: dict[str, Any]) -> Path:
    return (project_root() / config.get("edicoes", {}).get("pasta", "newsletter")).resolve()


def edition_subdir(config: dict[str, Any], name: str) -> str:
    """`edicoes.subpastas` (ex.: "{AAAA}/{MM}") → "2026/10" para a edição 2026-10-06."""
    pattern = config.get("edicoes", {}).get("subpastas", "")
    if not pattern or not EDITION_DIR_RE.match(name):
        return ""
    return pattern.replace("{AAAA}", name[:4]).replace("{MM}", name[5:7]).replace("{DD}", name[8:10])


def resolve_edition(value: str, config: dict[str, Any]) -> Path:
    path = Path(value)
    if not path.is_absolute():
        root = editions_root(config)
        candidates = [root / value, root / edition_subdir(config, Path(value).name) / Path(value).name]
        path = next((c for c in candidates if c.exists()), project_root() / value)
    path = path.resolve()
    root = editions_root(config)
    if root not in path.parents or not EDITION_DIR_RE.match(path.name):
        raise NewsletterError(f"A edição deve ser uma pasta {root.name}/AAAA-MM-DD[-sufixo]: {path}")
    if not path.is_dir():
        raise NewsletterError(f"Pasta da edição não encontrada: {path}")
    return path


def edition_date(edition: Path) -> str:
    return edition.name[:10]


def fill_date(template: str, iso: str) -> str:
    """Substitui {AAAA-MM-DD} e {DD/MM/AAAA} num modelo de nome."""
    year, month, day = iso.split("-")
    return template.replace("{AAAA-MM-DD}", iso).replace("{DD/MM/AAAA}", f"{day}/{month}/{year}")


def skill_path(relative: str) -> Path:
    return (SKILL_DIR / relative).resolve()


def section_by_id(config: dict[str, Any], section_id: str) -> dict[str, Any]:
    for section in config.get("secoes", []):
        if section.get("id") == section_id:
            return section
    raise NewsletterError(f"Seção não encontrada no config: {section_id}")


def metadata_status(edition: Path) -> str:
    meta = edition / "metadata.md"
    if not meta.exists():
        return ""
    for line in meta.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip().lstrip("-* ").strip()
        if stripped.lower().startswith("status:"):
            return stripped.split(":", 1)[1].strip().lower()
    return ""


# ---------------------------------------------------------------- credenciais

def env_file(config: dict[str, Any]) -> Path:
    platform = config.get("plataforma", {})
    rel = platform.get("credenciais") or f"private/{platform.get('tipo', 'plataforma')}.env"
    return project_root() / rel


class Credentials:
    """Valores de `private/<plataforma>.env`; variáveis de ambiente têm prioridade.

    Os valores nunca devem ser impressos ou gravados por quem chama.
    """

    def __init__(self, values: dict[str, str], source: Path) -> None:
        self._values = values
        self.source = source

    def get(self, key: str) -> str:
        return os.environ.get(key, "").strip() or self._values.get(key, "").strip()

    def require(self, key: str) -> str:
        value = self.get(key)
        if not value:
            raise NewsletterError(f"Credencial {key} ausente (arquivo {self.source} ou variável de ambiente).")
        return value


def load_env(config: dict[str, Any]) -> Credentials:
    """Lê `private/<plataforma>.env` no formato KEY=valor."""
    values: dict[str, str] = {}
    path = env_file(config)
    if path.is_file():
        for raw in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip().removeprefix("export ").strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key] = value
    return Credentials(values, path)


# ---------------------------------------------------------------- aprovação

def approval_settings(config: dict[str, Any]) -> dict[str, Any] | None:
    repo = config.get("aprovacao_repo") or {}
    if not repo.get("pasta"):
        return None
    return {
        "local": repo.get("local", "../aprovacoes-unid"),
        "pasta": repo["pasta"],
        "base_url": repo.get("base_url", "https://unidcom.github.io/aprovacoes-unid").rstrip("/"),
        "nome_arquivo": repo.get("nome_arquivo", "newsletter-{AAAA-MM-DD}.html"),
    }


def approval_target(config: dict[str, Any], edition: Path) -> tuple[Path, str, str] | None:
    """(caminho local do repositório, caminho relativo do arquivo, URL pública)."""
    settings = approval_settings(config)
    if not settings:
        return None
    local = Path(settings["local"])
    if not local.is_absolute():
        local = (project_root() / local).resolve()
    name = fill_date(settings["nome_arquivo"], edition_date(edition))
    suffix = edition.name[10:]
    if suffix:
        stem, dot, ext = name.rpartition(".")
        name = f"{stem}{suffix}{dot}{ext}" if dot else f"{name}{suffix}"
    rel = f"{settings['pasta']}/{name}"
    return local, rel, f"{settings['base_url']}/{rel}"
