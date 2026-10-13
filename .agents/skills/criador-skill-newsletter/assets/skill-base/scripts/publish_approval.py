#!/usr/bin/env python3
"""Publica a edição para aprovação no repositório `aprovacoes-unid` (GitHub Pages).

Uso:
  python publish_approval.py <pasta-da-edicao> [--sem-push] [--sem-espera] [--timeout 300]

1. Gera a cópia de aprovação sem as variáveis da plataforma (o link "ver no navegador"
   aponta para a própria página; o descadastro, que é individual, é removido).
2. Grava em `<aprovacao_repo.local>/<pasta>/<nome_arquivo>`.
3. Faz commit e push SÓ desse arquivo (outros clientes no repositório não são tocados).
4. Espera a URL servir exatamente o arquivo enviado (HTTP 200 sozinho não basta: a versão antiga também responde);
   na metade do tempo, pede um novo deploy do Pages. Depois grava `link_aprovacao` no payload.json.

--sem-push    grava e faz commit local, sem push (testes)
--sem-espera  não espera o HTTP 200 (testes; o link é gravado mesmo assim)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError

from _newsletter_common import (
    NewsletterError,
    approval_target,
    load_config,
    read_json,
    resolve_edition,
    write_json,
)
from validate_edition import validate


def anchor_pattern(var: str) -> re.Pattern[str]:
    return re.compile(r'<a\s+([^>]*?)href=["\']' + re.escape(var) + r'["\']([^>]*)>(.*?)</a>', re.I | re.S)


def approval_html(source: str, config: dict[str, Any], own_name: str) -> str:
    platform = config.get("plataforma", {})
    for var in platform.get("variaveis_espelho", []):
        source = anchor_pattern(var).sub(rf'<a \1href="{own_name}"\2>\3</a>', source)
    for var in platform.get("variaveis_descadastro", []):
        source = anchor_pattern(var).sub("<span>Descadastro disponível no e-mail recebido.</span>", source)
    for var in platform.get("variaveis_html", []):
        if var in source:
            raise NewsletterError(f"A cópia de aprovação ainda contém variável da plataforma: {var}")
    return source


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise NewsletterError(f"git {' '.join(args)} falhou: {(result.stderr or result.stdout).strip()[:500]}")
    return result.stdout.strip()


def request_pages_rebuild(repo: Path) -> bool:
    """Pede um novo deploy do GitHub Pages (o deploy às vezes falha ou trava do lado do GitHub)."""
    try:
        remote = git(repo, "remote", "get-url", "origin")
        match = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote)
        if not match:
            return False
        result = subprocess.run(["gh", "api", "-X", "POST", f"repos/{match[1]}/{match[2]}/pages/builds"],
                                capture_output=True, text=True, encoding="utf-8")
        return result.returncode == 0
    except (NewsletterError, OSError):
        return False


def wait_published(url: str, expected: str, timeout: int, repo: Path) -> tuple[bool, bool]:
    """Espera o link servir EXATAMENTE o arquivo enviado (não basta HTTP 200: a versão antiga também responde).

    Na metade do tempo sem atualizar, pede um novo deploy do Pages uma vez.
    Devolve (online, atualizado).
    """
    want = expected.replace("\r", "")
    deadline = time.monotonic() + timeout
    rebuild_at = time.monotonic() + timeout / 2
    online = rebuilt = False
    while True:
        try:
            req = request.Request(f"{url}?v={int(time.time())}", headers={"User-Agent": "newsletter-skill",
                                                                         "Cache-Control": "no-cache"})
            with request.urlopen(req, timeout=30) as r:
                online = r.status == 200
                if online and r.read().decode("utf-8", errors="replace").replace("\r", "") == want:
                    return True, True
        except (HTTPError, URLError, TimeoutError):
            pass
        if not rebuilt and time.monotonic() >= rebuild_at:
            rebuilt = request_pages_rebuild(repo)
        if time.monotonic() >= deadline:
            return online, False
        time.sleep(10)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("edicao")
    parser.add_argument("--sem-push", action="store_true")
    parser.add_argument("--sem-espera", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    try:
        config = load_config()
        edition = resolve_edition(args.edicao, config)
        target = approval_target(config, edition)
        if not target:
            raise NewsletterError("aprovacao_repo não configurado em config/newsletter.json.")
        repo, rel, url = target
        if not (repo / ".git").exists():
            raise NewsletterError(f"Repositório de aprovações não encontrado em {repo}. Clone aprovacoes-unid nesse caminho "
                                  "ou ajuste aprovacao_repo.local no config.")
        errors, _ = validate(edition, config)
        if errors:
            raise NewsletterError("Edição inválida: " + "; ".join(errors))

        dest = repo / rel
        html = approval_html((edition / "newsletter.html").read_text(encoding="utf-8"), config, dest.name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")

        git(repo, "add", "--", rel)
        committed = False
        if git(repo, "status", "--porcelain", "--", rel):
            git(repo, "commit", "-m", f"Aprovação: {rel}", "--", rel)
            committed = True
        pushed = False
        if not args.sem_push:
            git(repo, "push")
            pushed = True

        online = updated = None
        if not args.sem_espera:
            online, updated = wait_published(url, html, args.timeout, repo)
            if not online:
                raise NewsletterError(f"Arquivo publicado, mas {url} não respondeu HTTP 200 em {args.timeout}s. "
                                      "Conferir o GitHub Pages do aprovacoes-unid e rodar de novo.")
            if not updated:
                raise NewsletterError(f"{url} responde, mas ainda serve a versão ANTERIOR após {args.timeout}s "
                                      "(deploy do GitHub Pages falhou ou travou; já foi pedido um novo deploy). "
                                      "Conferir Actions/Pages do aprovacoes-unid e rodar de novo — não mandar o link antes.")

        payload_path = edition / "payload.json"
        payload = read_json(payload_path)
        payload["link_aprovacao"] = url
        write_json(payload_path, payload)
    except NewsletterError as exc:
        print(json.dumps({"ok": False, "erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "arquivo": str(dest), "link_aprovacao": url, "commit": committed,
                      "push": pushed, "http_200": online, "versao_nova_no_ar": updated}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
