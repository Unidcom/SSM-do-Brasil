#!/usr/bin/env python3
"""Valida (e opcionalmente monta) os artefatos de uma edição.

Uso:
  python validate_edition.py <pasta-da-edicao> [--sync] [--assunto "..."] [--pre-header "..."]

--sync   (re)escreve payload.json a partir de newsletter.html e plain-text.txt,
         preservando os campos já existentes (assunto, pré-header, link de aprovação).
         Na primeira vez, informe --assunto e --pre-header.

payload.json tem formato fixo, igual para todas as plataformas:
  nome_campanha, assunto, pre_header, html, texto, link_aprovacao

Sai com código 1 se houver erro. Avisos não bloqueiam.
"""

from __future__ import annotations

import argparse
import hashlib
import html as htmllib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

from _newsletter_common import (
    MOJIBAKE_RE,
    NewsletterError,
    edition_date,
    fill_date,
    load_config,
    read_json,
    resolve_edition,
    write_json,
)

EDITORIAL_PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
# Marcador esquecido do tipo "[TAG DA FONTE]": duas ou mais palavras em caixa alta.
# Siglas isoladas ("[ANEEL]", "[PDF]") são texto legítimo e não contam.
BRACKET_PLACEHOLDER = re.compile(r"\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9]+(?:[ _][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9]+)+\]")
FORBIDDEN_CSS = {
    "display:flex": re.compile(r"display\s*:\s*flex", re.I),
    "display:grid": re.compile(r"display\s*:\s*grid", re.I),
    "linear-gradient": re.compile(r"linear-gradient", re.I),
    "rgba()": re.compile(r"rgba\s*\(", re.I),
    "<script>": re.compile(r"<script", re.I),
}
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
SRC_ATTR = re.compile(r"\bsrc\s*=\s*[\"']([^\"']*)[\"']", re.I)
ALT_ATTR = re.compile(r"\balt\s*=\s*[\"'][^\"']*[\"']", re.I)
GMAIL_CLIP_BYTES = 102_000


def visible_text(html: str) -> str:
    """Texto que o leitor vê: sem <head>, tags e entidades; sem acento e em minúsculas."""
    body = re.sub(r"<head\b.*?</head>", " ", html, flags=re.I | re.S)
    text = htmllib.unescape(re.sub(r"<[^>]+>", " ", body))
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).lower()


def vocabulary_counts(html: str, vocab: dict[str, Any]) -> dict[str, dict[str, int]]:
    """Conta cada termo (radical, sem acento) no texto visível, depois de remover as expressões de `ignorar`."""
    text = visible_text(html)
    for phrase in vocab.get("ignorar", []):
        text = text.replace(visible_text(phrase), " ")
    return {group: {term: text.count(visible_text(term)) for term in vocab.get(group, [])}
            for group in ("priorizar", "secundario")}


COVER_RE = re.compile(
    r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']+)[\"'][^>]*>\s*(<img\b[^>]*object-fit\s*:\s*cover[^>]*>)", re.I)
SOURCE_LINK_RE = re.compile(r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']+)[\"'][^>]*>\s*Ler a fonte", re.I)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
TAKEAWAY_RE = re.compile(r">\s*0([1-3])\s*</span>\s*<br\s*/?>\s*([^<]*)", re.I)


def _plain(fragment: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def validate_layout(html: str, body: dict[str, Any], config: dict[str, Any],
                    errors: list[str], warnings: list[str]) -> None:
    """Estrutura do hero (mosaico + h1 + takeaways) e vínculo capa ↔ destaque do Radar."""
    opening = next((s for s in config.get("secoes", []) if s.get("id") == "abertura"), {})
    spec = opening.get("capas")
    if not spec:
        return
    expected = int(spec.get("quantidade", 3))

    covers = COVER_RE.findall(html)
    if len(covers) != expected:
        errors.append(f"Mosaico do topo com {len(covers)} capa(s) clicável(is); esperado {expected}.")
    for href, tag in covers:
        src = (SRC_ATTR.search(tag) or [None, ""])[1]
        if re.search(r"\.webp(?:[?#]|$)", src, re.I):
            warnings.append(f"Capa em WebP (Outlook desktop não renderiza): {src[:80]}")
        if not (re.search(r"\bwidth\s*=", tag, re.I) and re.search(r"\bheight\s*=", tag, re.I)):
            warnings.append(f"Capa sem width/height explícitos: {src[:80]}")

    sources = SOURCE_LINK_RE.findall(html)
    if len(sources) != expected:
        errors.append(f"Radar do setor com {len(sources)} destaque(s) com 'Ler a fonte'; esperado {expected}.")
    elif [h for h, _ in covers] != sources:
        errors.append("As capas do mosaico precisam linkar, na mesma ordem, para as URLs dos destaques do Radar.")

    headings = H1_RE.findall(html)
    if len(headings) != 1:
        errors.append(f"HTML com {len(headings)} <h1>; esperado exatamente 1 (título do hero).")
    elif body.get("assunto") and _plain(headings[0]) != _plain(body["assunto"]):
        errors.append("O <h1> do hero precisa ser igual ao assunto do payload.")

    takeaways = {n: _plain(t) for n, t in TAKEAWAY_RE.findall(html)}
    missing = [n for n in "123" if not takeaways.get(n)]
    if missing:
        errors.append(f"Takeaways do hero ausentes ou vazios: {', '.join('0' + n for n in missing)}.")


def campaign_name(config: dict[str, Any], edition: Path) -> str:
    template = config.get("nome_campanha") or f"{config.get('nome', 'Newsletter')} — {{AAAA-MM-DD}}"
    name = fill_date(template, edition_date(edition))
    suffix = edition.name[10:]
    return f"{name}{suffix}" if suffix else name


def sync_payload(edition: Path, config: dict[str, Any], subject: str | None, preheader: str | None) -> None:
    payload_path = edition / "payload.json"
    body = read_json(payload_path) if payload_path.exists() else {}
    if not isinstance(body, dict):
        raise NewsletterError("payload.json deve conter um objeto JSON.")
    body["nome_campanha"] = campaign_name(config, edition)
    if subject:
        body["assunto"] = subject
    if preheader is not None:
        body["pre_header"] = preheader
    if not body.get("assunto"):
        raise NewsletterError("Informe --assunto na primeira sincronização do payload.")
    body.setdefault("pre_header", "")
    body["html"] = (edition / "newsletter.html").read_text(encoding="utf-8")
    body["texto"] = (edition / "plain-text.txt").read_text(encoding="utf-8")
    body.setdefault("link_aprovacao", "")
    write_json(payload_path, body)


def validate(edition: Path, config: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    platform = config.get("plataforma", {})

    for name in ("newsletter.html", "plain-text.txt", "payload.json", "metadata.md"):
        if not (edition / name).is_file():
            errors.append(f"Artefato ausente: {name}")
    if errors:
        return errors, warnings

    try:
        html = (edition / "newsletter.html").read_text(encoding="utf-8")
        text = (edition / "plain-text.txt").read_text(encoding="utf-8")
        body = read_json(edition / "payload.json")
    except (UnicodeDecodeError, NewsletterError) as exc:
        return [f"Falha ao ler artefatos em UTF-8: {exc}"], warnings
    if not isinstance(body, dict):
        return ["payload.json deve conter um objeto JSON."], warnings

    if not html.lstrip().lower().startswith("<!doctype html"):
        errors.append("newsletter.html não começa com <!doctype html>.")
    if "</html>" not in html.lower():
        errors.append("newsletter.html não termina com </html> (documento incompleto).")

    for label, content in (("HTML", html), ("plain text", text)):
        leftovers = sorted(set(EDITORIAL_PLACEHOLDER.findall(content)))
        if leftovers:
            errors.append(f"Placeholders editoriais não preenchidos no {label}: {', '.join(leftovers)}")
        brackets = sorted(set(BRACKET_PLACEHOLDER.findall(content)))
        if brackets:
            errors.append(f"Marcadores entre colchetes no {label}: {', '.join(brackets)}")
        # "TODO" sozinho é palavra legítima em português ("TODO O BRASIL"); só o marcador conta.
        if re.search(r"TODO[(:]", content):
            errors.append(f"Marcador TODO encontrado no {label}.")
        if MOJIBAKE_RE.search(content):
            errors.append(f"{label} com provável corrupção de codificação (mojibake).")
        for forbidden in platform.get("proibido", []):
            if forbidden in content:
                errors.append(f"Texto proibido pela plataforma no {label}: {forbidden}")

    for var in platform.get("variaveis_html", []):
        if var not in html:
            errors.append(f"Variável de sistema obrigatória ausente no HTML: {var}")
    for var in platform.get("variaveis_texto", []):
        if var not in text:
            errors.append(f"Variável de sistema obrigatória ausente no plain text: {var}")

    for label, pattern in FORBIDDEN_CSS.items():
        if pattern.search(html):
            errors.append(f"HTML usa {label} (incompatível com clientes de e-mail).")
    if "\\<" in html or "\\>" in html:
        errors.append("HTML contém tags escapadas (\\< ou \\>).")
    if re.search(r"(?:src|href)=[\"']\[http", html):
        errors.append("HTML contém URL convertida indevidamente para Markdown.")
    if re.search(r"(?:src|href)=[\"'](?:file:|[A-Za-z]:\\)", html):
        errors.append("HTML contém caminho local (file:// ou C:\\).")

    for tag in IMG_TAG.findall(html):
        src_match = SRC_ATTR.search(tag)
        src = src_match.group(1) if src_match else ""
        if src.startswith("data:"):
            errors.append("Imagem embutida em base64 não é permitida.")
        elif not src.startswith("https://"):
            errors.append(f"Imagem sem URL HTTPS absoluta: {src or '(sem src)'}")
        if not ALT_ATTR.search(tag):
            warnings.append(f"Imagem sem alt: {src[:80]}")

    unknown = sorted(set(body) - {"nome_campanha", "assunto", "pre_header", "html", "texto", "link_aprovacao"})
    if unknown:
        errors.append(f"payload.json com campos fora do formato fixo: {', '.join(unknown)}")
    if body.get("nome_campanha") != campaign_name(config, edition):
        errors.append("payload.json com nome_campanha desatualizado — rode com --sync.")
    subject = body.get("assunto", "")
    limit = int(config.get("assunto_max", 70))
    if not subject:
        errors.append("payload.json sem assunto.")
    elif len(subject) > limit:
        errors.append(f"Assunto com {len(subject)} caracteres (máximo {limit}).")
    if not body.get("pre_header"):
        warnings.append("Pré-header vazio — os clientes de e-mail vão mostrar o começo do corpo no lugar.")
    if body.get("html") != html:
        errors.append("payload.json diverge de newsletter.html — rode com --sync.")
    if body.get("texto") != text:
        errors.append("payload.json diverge de plain-text.txt — rode com --sync.")

    validate_layout(html, body, config, errors, warnings)

    vocab = config.get("vocabulario") or {}
    if vocab.get("priorizar") and vocab.get("secundario"):
        counts = vocabulary_counts(html, vocab)
        prio, sec = sum(counts["priorizar"].values()), sum(counts["secundario"].values())
        if prio <= sec:
            errors.append(f"Vocabulário: termos prioritários {counts['priorizar']} ({prio}) precisam aparecer mais "
                          f"que os secundários {counts['secundario']} ({sec}) — reescrever com mais ênfase "
                          f"nos prioritários (config → vocabulario).")

    if config.get("verificar_links"):
        report_path = edition / "links-report.json"
        if not report_path.is_file():
            errors.append("Links não verificados — rode check_links.py (verificar_links: true).")
        else:
            report = read_json(report_path, default={})
            if report.get("html_sha256") != hashlib.sha256(html.encode("utf-8")).hexdigest():
                errors.append("links-report.json é de outra versão do HTML — rode check_links.py de novo.")
            elif not report.get("ok"):
                errors.append(f"Verificação de links com {len(report.get('erros', []))} erro(s) — ver links-report.json.")
            for w in report.get("avisos", []):
                warnings.append(f"Link: {w}")

    size = len(html.encode("utf-8"))
    if size > GMAIL_CLIP_BYTES:
        warnings.append(f"HTML com {size // 1024} KB — o Gmail corta mensagens acima de ~102 KB.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("edicao")
    parser.add_argument("--sync", action="store_true")
    parser.add_argument("--assunto")
    parser.add_argument("--pre-header")
    args = parser.parse_args()
    try:
        config = load_config()
        edition = resolve_edition(args.edicao, config)
        if args.sync:
            sync_payload(edition, config, args.assunto, args.pre_header)
        errors, warnings = validate(edition, config)
    except NewsletterError as exc:
        print(json.dumps({"ok": False, "erros": [str(exc)]}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({"ok": not errors, "edicao": str(edition), "erros": errors, "avisos": warnings},
                     ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
