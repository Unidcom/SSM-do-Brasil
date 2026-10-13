#!/usr/bin/env python3
"""Verifica todos os links e imagens de uma edição e grava `links-report.json`.

Uso:
  python check_links.py <pasta-da-edicao> [--esperado "URL=texto"]...

Para cada `href` e `<img src>` do newsletter.html (exceto variáveis da plataforma,
mailto:, tel: e âncoras), faz um GET com user-agent de navegador, segue redirecionamentos
e registra status, URL final, tipo de conteúdo e título da página.

Erros (bloqueiam a edição):
  - domínio inexistente, sem conexão ou timeout;
  - HTTP 4xx/5xx (exceto 401/403/429, que viram aviso — o site bloqueou o robô);
  - página de domínio estacionado/à venda;
  - `<img>` cujo conteúdo não é imagem;
  - `--esperado`: o texto não aparece no título nem no corpo da página
    (comparação sem acento e sem caixa). Use para provar que o link é do evento/item certo.

Avisos (conferir manualmente e registrar em metadata.md):
  - redirecionamento para outro domínio (preferir a URL final no HTML);
  - bloqueio do robô (401/403/429).

O relatório guarda o hash do HTML: se o HTML mudar, a verificação precisa rodar de novo.
"""

from __future__ import annotations

import argparse
import hashlib
import html as htmllib
import json
import re
import socket
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

from _newsletter_common import NewsletterError, load_config, resolve_edition, write_json

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HREF = re.compile(r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']+)[\"']", re.I)
IMG = re.compile(r"<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
PARKED = ("domain is for sale", "this domain is for sale", "buy this domain", "comprar este dominio",
          "este dominio esta a venda", "dominio a venda", "parked domain", "domain parking",
          "hugedomains", "sedo.com", "dan.com", "afternic")
SOFT_BLOCK = {401, 403, 429}
# Encurtadores/links de app que sempre redirecionam para o domínio do serviço.
KNOWN_REDIRECTS = {("wa.me", "whatsapp.com"), ("bit.ly", "bit.ly"), ("youtu.be", "youtube.com"),
                   ("instagram.com", "instagram.com"), ("fb.me", "facebook.com")}
MAX_BYTES = 1_500_000


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", htmllib.unescape(text)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).lower().strip()


def base_domain(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    host = host[4:] if host.startswith("www.") else host
    parts = host.split(".")
    # exemplo.com.br → exemplo.com.br; sub.exemplo.com → exemplo.com
    keep = 3 if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in {"com", "org", "net", "gov", "edu"} else 2
    return ".".join(parts[-keep:])


def collect(html: str) -> list[tuple[str, str]]:
    found: dict[str, str] = {}
    for kind, pattern in (("imagem", IMG), ("link", HREF)):
        for raw in pattern.findall(html):
            url = htmllib.unescape(raw).strip()
            if (not url or url.startswith(("#", "mailto:", "tel:")) or "{$" in url or "{{" in url
                    or not url.startswith(("http://", "https://"))):
                continue
            found.setdefault(url, kind)
    return list(found.items())


def fetch(url: str) -> dict:
    req = request.Request(url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "pt-BR,pt;q=0.9"})
    last_error = ""
    # Sites de feira ficam lentos perto do evento (handshake TLS > 25 s): 3 tentativas de 45 s com pausa.
    for attempt in range(3):
        if attempt:
            time.sleep(5 * attempt)
        try:
            with request.urlopen(req, timeout=45) as resp:
                ctype = resp.headers.get("Content-Type", "")
                body = resp.read(MAX_BYTES) if "html" in ctype or "text" in ctype else b""
                return {"status": resp.status, "url_final": resp.geturl(), "tipo": ctype,
                        "corpo": body.decode("utf-8", errors="replace")}
        except HTTPError as exc:
            return {"status": exc.code, "url_final": exc.geturl() or url, "tipo": exc.headers.get("Content-Type", ""),
                    "corpo": ""}
        except (URLError, TimeoutError, ConnectionError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            last_error = str(reason)
            if isinstance(reason, socket.gaierror):
                break  # domínio não existe: repetir não adianta
    return {"status": None, "url_final": url, "tipo": "", "corpo": "", "falha": last_error}


def check(url: str, kind: str, expected: list[str]) -> dict:
    r = fetch(url)
    title = norm(TITLE.search(r["corpo"]).group(1)) if TITLE.search(r["corpo"]) else ""
    body = norm(re.sub(r"<[^>]+>", " ", r["corpo"]))
    result = {"url": url, "tipo_ref": kind, "status": r["status"], "url_final": r["url_final"],
              "conteudo": r["tipo"].split(";")[0], "titulo": title[:160], "erros": [], "avisos": []}

    if r["status"] is None:
        falha = r.get("falha", "")
        if "getaddrinfo" in falha or "Name or service not known" in falha:
            result["erros"].append(f"domínio não existe: {falha[:120]}")
        elif "timed out" in falha.lower():
            result["erros"].append("site lento: não respondeu em 3 tentativas de 45 s — abrir no navegador; "
                                   "se abrir, rodar check_links.py de novo")
        else:
            result["erros"].append(f"sem resposta (fora do ar ou recusou a conexão): {falha[:120]}")
        return result
    if r["status"] in SOFT_BLOCK:
        result["avisos"].append(f"HTTP {r['status']}: o site bloqueou a verificação automática — abrir no navegador e confirmar")
    elif r["status"] >= 400:
        result["erros"].append(f"HTTP {r['status']}")
        return result
    if kind == "imagem" and r["status"] < 400 and not result["conteudo"].startswith("image/"):
        result["erros"].append(f"imagem com conteúdo '{result['conteudo'] or 'desconhecido'}'")
    if any(p in body[:5000] or p in title for p in PARKED):
        result["erros"].append("página de domínio estacionado/à venda")
    final_domain = base_domain(r["url_final"])
    if (kind == "link" and final_domain != base_domain(url)
            and (base_domain(url), final_domain) not in KNOWN_REDIRECTS):
        result["avisos"].append(f"redireciona para outro domínio: {r['url_final']} — usar a URL final no HTML")
    for text in expected:
        if r["status"] in SOFT_BLOCK:
            result["avisos"].append(f"conteúdo esperado '{text}' não pôde ser conferido (bloqueio) — conferir manualmente")
        elif norm(text) not in title and norm(text) not in body:
            result["erros"].append(f"a página não menciona '{text}' — link provavelmente não é deste evento/item")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("edicao")
    parser.add_argument("--esperado", action="append", default=[], metavar="URL=texto",
                        help="texto que a página do URL precisa conter (repetível)")
    args = parser.parse_args()
    try:
        config = load_config()
        edition = resolve_edition(args.edicao, config)
        html = (edition / "newsletter.html").read_text(encoding="utf-8")
        expected: dict[str, list[str]] = {}
        for item in args.esperado:
            if "=" not in item:
                raise NewsletterError(f"--esperado precisa ser URL=texto: {item}")
            url, text = item.split("=", 1)
            expected.setdefault(url.strip(), []).append(text.strip())
        refs = collect(html)
        missing = sorted(set(expected) - {u for u, _ in refs})
        results = [check(url, kind, expected.get(url, [])) for url, kind in refs]
        errors = [f"{r['url']}: {e}" for r in results for e in r["erros"]]
        errors += [f"{u}: --esperado para URL que não está no HTML" for u in missing]
        warnings = [f"{r['url']}: {w}" for r in results for w in r["avisos"]]
        report = {"ok": not errors, "verificado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                  "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
                  "total": len(results), "erros": errors, "avisos": warnings, "resultados": results}
        write_json(edition / "links-report.json", report)
    except (NewsletterError, OSError) as exc:
        print(json.dumps({"ok": False, "erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({k: report[k] for k in ("ok", "total", "erros", "avisos")}, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
