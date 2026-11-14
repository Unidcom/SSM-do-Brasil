#!/usr/bin/env python3
"""Validate alt text for Markdown images in a blog article."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
GENERIC_ALT = {
    "image",
    "imagem",
    "photo",
    "foto",
    "graphic",
    "grafico",
    "gráfico",
    "illustration",
    "ilustracao",
    "ilustração",
    "banner",
    "cover",
    "capa",
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate empty, generic, duplicated, or weak alt text in Markdown images."
    )
    parser.add_argument("article", type=Path, help="Markdown article to validate")
    args = parser.parse_args()

    if not args.article.is_file():
        print(f"ERRO: artigo nao encontrado: {args.article}", file=sys.stderr)
        return 2

    content = args.article.read_text(encoding="utf-8")
    images = IMAGE_PATTERN.findall(content)
    if not images:
        print("AVISO: nenhuma imagem Markdown encontrada.")
        return 0

    normalized = [normalize(alt) for alt, _ in images]
    duplicates = {alt for alt, count in Counter(normalized).items() if alt and count > 1}
    errors: list[str] = []
    warnings: list[str] = []

    for index, ((alt, source), normalized_alt) in enumerate(zip(images, normalized), start=1):
        label = f"imagem {index} ({source})"
        if not normalized_alt:
            errors.append(f"{label}: alt text vazio")
            continue
        if normalized_alt in GENERIC_ALT:
            errors.append(f"{label}: alt text generico: {alt!r}")
        if normalized_alt in duplicates:
            errors.append(f"{label}: alt text duplicado: {alt!r}")
        if len(alt.strip()) < 35:
            warnings.append(f"{label}: alt text curto; descreva melhor a funcao editorial")
        if len(alt.strip()) > 200:
            warnings.append(f"{label}: alt text longo; considere resumir")
        if re.match(r"^(imagem|foto|arte|grafico|gráfico)\s+de\b", normalized_alt):
            warnings.append(f"{label}: evite iniciar com 'imagem/foto/arte/grafico de'")

    for message in errors:
        print(f"ERRO: {message}")
    for message in warnings:
        print(f"AVISO: {message}")

    if errors:
        print(f"FALHOU: {len(errors)} erro(s), {len(warnings)} aviso(s).")
        return 1

    print(f"OK: {len(images)} imagem(ns) com alt text unico e nao vazio; {len(warnings)} aviso(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
